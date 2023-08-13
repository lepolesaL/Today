
import {
  Container, 
  Heading, 
  SimpleGrid,
  Box,
  Button,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  useDisclosure,
  Textarea,
  Stack,
  Text,
  Input,
  Select
} from '@chakra-ui/react'
import { AddIcon } from '@chakra-ui/icons'
import { DragDropContext } from 'react-beautiful-dnd'
import React, { useEffect, useState } from 'react';
import { Column } from './Column';
import axios from 'axios';

// const Columns = {
//   'column-1': {id: "column-1",
//    name: "todo",
//    color: "red",
//    tasks: []
//   },
//   'column-2': {id: "column-2", 
//   name: "today", 
//   color: "yellow",
//   tasks: []
//   },
//   'column-3': {id: "column-3",
//    name: "done", 
//    color: "green",
//    tasks: []
//   },
// }

// const columnOrder = ['column-1', 'column-2', 'column-3']

// const isToday = date => {
//   const today = new Date()
//   return date.getDate() === today.getDate() && 
//       date.getMonth() === today.getMonth() && 
//       date.getFullYear() === today.getFullYear()
// }

export const Today = () => {
  const [todos, setTodos] = useState({})
  const [columns, setColumns] = useState({});
  const { isOpen, onOpen, onClose } = useDisclosure()
  const [todoTitle, setTodoTitle] = useState('');
  const [todoDescription, setTodoDescription] = useState('');
  const [loadTodos, setLoadTodos] = useState(true)
  const [projects, setProjects] = useState([])
  const [selectedProject, setSelectedProject] = useState('')
  // const { isOpen, onOpen, onClose } = useDisclosure(

  const getItemStyle = (isDragging, draggableStyle) => ({
    // some basic styles to make the items look a bit nicer
    userSelect: 'none',
    padding: 10,
    margin: `0 0 8px 0`,

    // change background colour if dragging
    background: isDragging ? 'lightgreen' : 'grey',

    // styles we need to apply on draggables
    ...draggableStyle,
  });

  const onDragEnd = async (result) => {
    const { destination, source, draggableId } = result

    if (!destination) {
        return
    }
    if (
        destination.droppableId === source.droppableId &&
        destination.index === source.index
    ) {
        return
    }
    if (destination.droppableId === source.droppableId && destination.index !== source.index) {
      var col = columns[source.droppableId]
      col.todos.splice(source.index, 1)
      col.todos.splice(destination.index, 0, draggableId)
      let response = await axios.patch(`${process.env.REACT_APP_API_URL}/columns/${col.id}/`, col.todos)
      if (response.status) {
        setColumns(prev => ({
          ...prev,
          [destination.droppableId]: col
        }));
      }
    } else if (destination.droppableId !== source.droppableId) {
      var srcCol = columns[source.droppableId]
      var destCol = columns[destination.droppableId]
      srcCol.todos.splice(source.index, 1)
      destCol.todos.splice(destination.index, 0, draggableId)
      let scrResponse = await axios.patch(`${process.env.REACT_APP_API_URL}/columns/${srcCol.id}/`, srcCol.todos)
      let destResponse = await axios.patch(`${process.env.REACT_APP_API_URL}/columns/${destCol.id}/`, destCol.todos)
      if (scrResponse.status && destResponse.status) {
        try {
          await axios.patch(`${process.env.REACT_APP_API_URL}/todos/${draggableId}/`, {status: destCol.name})
        } catch(e) {
          console.log(e)
        }
        setColumns(prev => ({
          ...prev,
          [destination.droppableId]: destCol,
          [source.droppableId]: srcCol,
        }));
      }
    }
  }

  const addTask = () => {
    if (!!todoTitle && !!todoDescription && !!selectedProject) {
      axios.post(`${process.env.REACT_APP_API_URL}/todos/`, {
        title: todoTitle,
        description: todoDescription,
        project_id: selectedProject,
        status: "today"
      })
      .then((taskResponse) => {
          const todoId = taskResponse.data.id
          var newTodo = {}
          newTodo.id = todoId
          newTodo.title = todoTitle
          newTodo.description = todoDescription
          newTodo.status = "today"
          // newTodo.tasks = []
          setTodos(prev => ({
            ...prev,
            [todoId]: newTodo
          }));
          var newColumns = columns
          var columnId = Object.keys(newColumns)[1]
          var column = newColumns[columnId]
          column['todos'].splice(0,0,todoId)
          axios.patch(`${process.env.REACT_APP_API_URL}/columns/${column.id}/`, column.todos)
          .then((data)=> {
            setColumns(prev => ({
              ...prev,
              [columnId]: column
            }));
            onClose()
          })
          .catch((error) => {
            console.log(error)
          })
      })
      .catch((error)=>{console.log(error)})
    }
  }

  const updateColumns = async(column) => {
    setColumns(prev => ({
      ...prev,
      [column.id]: column
    }));
  }

  useEffect(() => {
    const loadTodos = async () => {
      const response = await axios.get(`${process.env.REACT_APP_API_URL}/todos/`)
      var todoList = response.data
      var todos = Object.fromEntries(todoList.map(item => [item.id, item]));
      setTodos(todos)
      setLoadTodos(false)
    }
    loadTodos()
   }, [loadTodos]);

   useEffect(() => {
    var loadColumns = async() => {
      const response = await axios.get(`${process.env.REACT_APP_API_URL}/columns/`)
      var columnList = response.data
      var columns = Object.fromEntries(columnList.map(item => [item.id, item]));
      setColumns(columns)
    }
    !!columns && loadColumns()
   }, [loadTodos])

   useEffect(() => {
      const loadProjects = async() => {
        const response = await axios.get(`${process.env.REACT_APP_API_URL}/projects/`)
        const projects = response.data
        setProjects(projects)
      }
      loadProjects()
   }, [])

  return(
    <>
    {
      loadTodos ?
      <Container></Container>
    : 
    <Container maxWidth="container.xl" bg="rgba(255, 255, 255, 0.8)" minHeight="calc(100vh - 80px)" overflow="auto" my={10} display="flex" flexDirection="column">
    <Heading
      fontSize={{ base: '3xl', md: '4xl', lg: '5xl' }}
      textAlign="center"
      fontWeight="bold"
      color="brand.dark"
      my={8}
    >
      Dashboard
    </Heading>
    <Box p={4}>
      <Button colorScheme="brand" onClick={onOpen} leftIcon={<AddIcon />}>
        Add Todo
      </Button>
    </Box>
    <DragDropContext onDragEnd={onDragEnd}>
      <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6} mb={10} h="100%" overflow="auto">
        {Object.keys(columns).map((key, index) => {
          const columnTodos = columns[key].todos.map((todoId) => todos[todoId]).filter(n => n !== undefined);
          return (
            <Column
              key={index}
              index={index}
              column={columns[key]}
              tasks={columnTodos}
              updateColumns={updateColumns}
            />
          );
        })}
      </SimpleGrid>
    </DragDropContext>
  </Container>
    }
    <Modal isOpen={isOpen}  size={'lg'} onClose={onClose}>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Add Todo</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          <Stack p={2} gap={2}>
            <Text>Title:</Text>
            <Input placeholder='Add todo name' defaultValue={""} onChange={e => setTodoTitle(e.currentTarget.value)}/>
            <Stack>
              <Text>Project:</Text>
              <Select placeholder='Select Project' onChange={e => setSelectedProject(e.currentTarget.value)}>
                {projects.map((project) => <option key={project.id} value={project.id}>{project.name}</option>)}
              </Select>
            </Stack>
            <Stack>
              <Text>Description:</Text>
              <Textarea  onChange={e => setTodoDescription(e.currentTarget.value)}/>
            </Stack>
          </Stack>
        </ModalBody>

        <ModalFooter>
          <Button  mr={3} onClick={onClose}>
            Close
          </Button>
          <Button colorScheme='blue' variant='ghost' onClick={addTask}>Save</Button>
        </ModalFooter>
      </ModalContent>
    </Modal> 
    </>
  )
}