import {
  Box, 
  Heading, 
  Stack, 
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  Button,
  Textarea,
  Text,
  Input,
  Divider,
  HStack,
  Checkbox
} from '@chakra-ui/react';
import React, { useEffect, useState, useRef} from 'react';
import axios from 'axios';
import { AddIcon} from '@chakra-ui/icons';
import { Comment } from './Comment';

export const TodoModal = ({ isOpen, onClose, todo}) => {
  const [comments, setComments] = useState([])
  const [newComments, setNewComments] = useState([])
  const [newCommentCount, setNewCommentCount] = useState(0);
  const [taskList, setTaskList] = useState([])
  const [newTasks, setNewTasks] = useState([])
  const [newTaskCount, setNewTaskCount] = useState(0);
  const taskInput = useRef(null)
  const descriptionInput = useRef(null)
  const commentInput = useRef(null)


  useEffect(() => {
    const loadTasks = async () => {
      const response = await axios.get(`${process.env.REACT_APP_API_URL}/todos/${todo.id}/tasks/`)
      setTaskList(response.data)
    }
    loadTasks()
  }, [])

  useEffect(() => {
    const loadComments = async () => {
      const response = await axios.get(`${process.env.REACT_APP_API_URL}/todos/${todo.id}/comments/`)
      setComments(response.data)
    }
    loadComments()
  }, [])

  const updateTodo = () => {
    let payload = {
      description: descriptionInput.current.value,
      new_tasks: newTasks,
      updated_tasks: taskList,
      new_comments: newComments,
    }
    axios.patch(`${process.env.REACT_APP_API_URL}/todos/${todo.id}/`, payload)
    .then(() => {
      onClose()
      setNewComments([])
      setNewCommentCount(0)
      setNewTasks([])
      setNewTaskCount(0)
    })
    .catch((e) => console.log(e))
  }

  const updateTask = (e, id) => {
    const taskIndex = taskList.findIndex((task) => task.id === id)
    const updatedTask = {...taskList[taskIndex], status: e.target.checked}
    const newTaskList = [...taskList]
    newTaskList[taskIndex] = updatedTask
    setTaskList(newTaskList)
  }

  const addNewTask = (e) => {
    if (e.key === 'Enter') {
      let taskList = newTasks
      const newTask = {title: taskInput.current.value, status: false}
      taskList.unshift(newTask)
      setNewTasks(taskList)
      setNewTaskCount(prevCount => prevCount + 1)
      taskInput.current.value=''
      taskInput.current.hidden = true
    }
  }

  const addNewComment = async(e) => {
    if (e.key === 'Enter') {
      let commentList = newComments
      commentList.unshift(commentInput.current.value)
      setNewComments(commentList)
      setNewCommentCount(prevCount => prevCount + 1)
      commentInput.current.value=''

    }
  }

  const handleCancel = () => {
    onClose()
    setNewComments([])
    setNewCommentCount(0)
    setNewTasks([])
    setNewTaskCount(0)
  }


  return (
    <Modal isOpen={isOpen}  size={'lg'} onClose={onClose}>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Task Details</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          <Stack p={2} gap={2}>
            <Heading size='sm'>{todo.title}</Heading>
            <Stack>
              <Text>Description:</Text>
              <Textarea defaultValue={todo.description} ref={descriptionInput}/>
            </Stack>
            <Stack>
              <HStack>
                <Text fontSize='sm'>Tasks</Text>
                <Divider />
                <AddIcon onClick={() => taskInput.current.hidden = false}/>
              </HStack>
              <Stack>
                <Input 
                  placeholder='small size' 
                  size='sm'
                  ref={taskInput} 
                  hidden
                  onKeyDown={(e) => addNewTask(e)}
                  />
                  { 
                    [...Array(newTaskCount)].map((_,index) => <Checkbox defaultChecked={newTasks[index].status} key={index}>{newTasks[index].title}</Checkbox>)
                  }
                  {
                    taskList.map(task => 
                      <Checkbox key={task.id} defaultChecked={task.status} onChange={(e) => updateTask(e, task.id)}>{task.title}</Checkbox>
                    )
                  }
              </Stack>
            </Stack>
            <Stack>
            <Text>Comments:</Text>
              <Input placeholder='Add Comment' defaultValue={""} ref={commentInput} onKeyDown={(e) => addNewComment(e)}/>
              <Box border={1}>
                { 
                  [...Array(newCommentCount)].map((_,index) => 
                    <Comment comment={newComments[index]} key={index} date={new Date()} />
                  )
                }
                {
                  comments.reverse().map(comment =>
                    <Comment comment={comment.text} key={comment.id} date={comment.created_at}/>
                  )
                }

              </Box>
            </Stack>
          </Stack>
        </ModalBody>

        <ModalFooter>
          <Button  mr={3} onClick={handleCancel}>
            Cancel
          </Button>
          <Button colorScheme='blue' variant='ghost' onClick={updateTodo}>Save</Button>
        </ModalFooter>
      </ModalContent>
    </Modal> 
    )
}