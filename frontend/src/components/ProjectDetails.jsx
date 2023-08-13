import {
    Container, 
    Heading, 
    Button,
    TableContainer,
    Table,
    Thead,
    Tr,
    Th,
    Tbody,
    Td} from '@chakra-ui/react'
import { useEffect, useState } from 'react'
import axios from 'axios'
import { useParams } from 'react-router-dom'

  
  
  export const ProjectDetails= () => {
    const [project, setProject] = useState(null)
    const [todos, setTodos] = useState([])
    const [loading, setLoading] = useState(true)
    const {projectId } = useParams()
    useEffect(() => {
        const fetchProjectById = (projectId) => {
            axios.get(`${process.env.REACT_APP_API_URL}/projects/${projectId}/`)
            .then((response) => {
                setProject(response.data)
                setLoading(false)
            })
        }

        fetchProjectById(projectId)
    }, [])

    useEffect(() => {
        const fetchTodosByProjectId = (projectId) => {
            axios.get(`${process.env.REACT_APP_API_URL}/todos/by_project/${projectId}/`)
            .then((response) => {
              var todos = response.data
              todos.forEach((element, index) => {
                todos[index].accumulated_time = element.accumulated_time === null ? 0 :  element.accumulated_time 
              });
              setTodos(todos)
            })
            .catch((error)=>{console.log(error)})
        }
        fetchTodosByProjectId(projectId)
    }, [])

    const deleteTodoFromProject = (id) => {
      axios.delete(`${process.env.REACT_APP_API_URL}/todos/${id}/`)
      .then(() => {
       console.log('deleted')
      })
    }
      
    return(
    <>
      {
      loading ?
      <Container></Container>
      : 
        <Container maxWidth={'container.lg'}  bg={'rgba(237,244,242, 0.8)'} mb={'10'} mt={'10'}>
         <Heading
          fontSize={{base: '4xl', sm: '5xl', md: '5xl'}}
          textAlign={'center'}
          fontWeight={'bold'}
          bgClip={'text'}
          textColor={'black'}
          mt={4} 
        >
          {project.name}
        </Heading>
        <TableContainer border={'2px'} mt={'10'} borderRadius={'lg'} mx={'10'}>
          <Table variant='simple'>
            {/* <TableCaption>Imperial to metric conversion factors</TableCaption> */}
              <Thead>
              <Tr>
                <Th>Title</Th>
                <Th>Status</Th>
                <Th isNumeric>Duration</Th>
                <Th>Action</Th>
              </Tr>
              </Thead>
              <Tbody>
                {todos.map((todo)=>
                  <Tr key={todo.id}>
                    <Td>{todo.title}</Td>
                    <Td>{todo.status}</Td>
                    <Td isNumeric>{todo.accumulated_time}</Td>
                    <Td><Button onClick={e => deleteTodoFromProject(todo.id)}>Delete</Button></Td>
                  </Tr>
                )}
              </Tbody>
              {/* <Tfoot>
              <Tr>
                <Th>To convert</Th>
                <Th>into</Th>
                <Th isNumeric>multiply by</Th>
              </Tr>
              </Tfoot> */}
          </Table>
        </TableContainer>
      </Container>
    }
    </>
    )
  }