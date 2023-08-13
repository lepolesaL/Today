import {
    Box, 
    Stack, 
    useDisclosure,
    Button,
    Text,
    Progress,
    Flex,
    HStack,
    IconButton
  } from '@chakra-ui/react'
import { DeleteIcon, ChatIcon } from '@chakra-ui/icons'
import { Draggable } from 'react-beautiful-dnd'
import React, { useEffect, useState} from 'react';
import axios from 'axios';
import { TodoModal } from './TodoModal';


  export const Todo = ({todo, index, columnId, deleteFromColumn}) => {

    const { isOpen, onOpen, onClose } = useDisclosure()
    const [progress, setProgress] = useState(100)
    const [numCompletedTask, setNumCompletedTask] = useState(0)
    const [totalTasks, setTotalTasks] = useState(0)
    const [startTime, setStartTime] = useState(null)
    const [isTimerStarted, setIsTimerStarted] = useState(false) 
    const [timeInterval, setTimeInterval] = useState(null)
    const [timer, setTimer] = useState(null)
    const [accumulatedTimeInSeconds, setAccumulatedTimeInSeconds] = useState(0)
    const [pauseButton, setPauseButton] = useState('Pause')

    useEffect(() => {
      const setTaskProgress = () => {
        let numberOfTasks = todo.num_tasks
        if (numberOfTasks !== undefined && numberOfTasks !== 0) {
          let completedTasks = todo.num_completed_tasks
          let progress = completedTasks/numberOfTasks * 100
          setNumCompletedTask(completedTasks)
          setTotalTasks(numberOfTasks)
          setProgress(progress)
        }
      }
      setTaskProgress()
    },[])

    useEffect(() => {
      const setupStartTime = async () => {
        const todoTimer =  await getTodoTimer()
        if (todoTimer !== null && todoTimer.status !== 'stopped') {
          setIsTimerStarted(true)
          if (todoTimer.status === 'started') {
            setStartTime(new Date(todoTimer.created_at))
          } else if (todoTimer.status === 'resumed') {
            setStartTime(new Date(todoTimer.modified_at))
            setAccumulatedTimeInSeconds(todoTimer.accumulated_time)
          } else if (todoTimer.status === 'paused') {
            setAccumulatedTimeInSeconds(todoTimer.accumulated_time)
            var time = (todoTimer.accumulated_time * 1000)
            var formattedTime = timeFormat(time)
            setTimer(`${formattedTime.hours}:${formattedTime.minutes}:${formattedTime.seconds}`)
            setPauseButton('Resume')
          }
        }
      }
      startTime === null && setupStartTime()
    }, [])

    useEffect(() => {
      const startTimer =  () => {
      
        var timeInterval = setInterval(() => {
          var time =  (Date.now() - startTime) + (accumulatedTimeInSeconds * 1000)
          var formattedTime = timeFormat(time)
          setTimer(`${formattedTime.hours}:${formattedTime.minutes}:${formattedTime.seconds}`)
        }, 1000);
        setTimeInterval(timeInterval)
      }
      startTime !== null && startTimer()
      return async() => {
        if(timeInterval !== null) {
          const todoTimer =  await getTodoTimer()
          axios.patch(`${process.env.REACT_APP_API_URL}/todos/${todo.id}/todo_timer/${todoTimer.id}/`, {
            status: 'started',
            accumulated_time:  accumulatedTotalSeconds()
          })
          clearInterval(timeInterval)
          setTimeInterval(null)
        }
      }
    },[startTime])


  // Format time in milliseconds to hh:mm:ss
  const timeFormat = (time) => {
    var hours = Math.floor((time / (1000 * 60 * 60)) % 24);
    var minutes = Math.floor((time / 1000 / 60) % 60);
    var seconds = Math.floor((time / 1000) % 60);
    var hourStr = hours.toString().length < 2 ? `0${hours}` : hours
    var minuteStr = minutes.toString().length < 2 ? `0${minutes}` : minutes
    var secondStr = seconds.toString().length < 2 ? `0${seconds}` : seconds
    return {
      hours: hourStr,
      minutes: minuteStr,
      seconds: secondStr
    }
  }

  const startTimer = () => {
    const data = {
      status: 'started'
    }
    axios.post(`${process.env.REACT_APP_API_URL}/todos/${todo.id}/todo_timer/`, data)
    .then(() => {
      setStartTime(Date.now())
      setIsTimerStarted(true)
    }).catch((e) => console.log(e))
  }
  
  const getTodoTimer = async () => {
    //  Get timer
    try {
      const response = await axios.get(`${process.env.REACT_APP_API_URL}/todos/${todo.id}/todo_timer/`)
      return response.data
    } catch(error) {
      // if(error.status)
      console.log(error)
    }
    return null
  }

  const accumulatedTotalSeconds = () => {
    var splitTimerStr = timer.split(':')
    var hours = parseInt(splitTimerStr[0])
    var minutes = parseInt(splitTimerStr[1])
    var seconds = parseInt(splitTimerStr[2])

    return (hours * 3600) + (minutes * 60) + seconds
  }

  const deleteTodo = () => {
    axios.delete(`${process.env.REACT_APP_API_URL}/todos/${todo.id}/`)
    .then(() => {
      deleteFromColumn(index)
    })
  }

  const stopTimer = async () => {
    const todoTimer =  await getTodoTimer()
    axios.delete(`${process.env.REACT_APP_API_URL}/todos/${todo.id}/todo_timer/${todoTimer.id}/`)
    .then(() => {
      setStartTime(null)
      setIsTimerStarted(false)
    }).catch(e => console.log(e))
    clearInterval(timeInterval)
    setTimeInterval(null)
  }

  const pauseResumeTimer = async (e) => {
    let buttonName = e.target.innerText;
    const todoTimer =  await getTodoTimer()
    if (buttonName === 'Resume') {
      axios.patch(`${process.env.REACT_APP_API_URL}/todos/${todo.id}/todo_timer/${todoTimer.id}/`, {
        status: 'resumed',
        accumulated_time:  todoTimer.accumulated_time
      })
      .then(() => {
        setStartTime(Date.now())
        setAccumulatedTimeInSeconds(todoTimer.accumulated_time)
        setPauseButton('Pause')
      }).catch((e) => console.log(e))
    } else if (buttonName === "Pause") {
      axios.patch(`${process.env.REACT_APP_API_URL}/todos/${todo.id}/todo_timer/${todoTimer.id}/`, {
        status: 'paused',
        accumulated_time:  accumulatedTotalSeconds()
      })
      .then(() => {
        clearInterval(timeInterval)
        setTimeInterval(null)
        setPauseButton('Resume')
      }).catch((e) => console.log(e))
    }
  }

  return (
      <>
      <Draggable
          key={todo.id}
          draggableId={todo.id}
          index={index}>
          {(provided, snapshot) => (
          <Box
          onDoubleClick={onOpen}
          w="full"
          rounded="lg"
          p={3}
          bg="white"
          boxShadow="md"
          transition="all 0.2s"
          _hover={{ transform: 'translateY(-2px)', boxShadow: 'lg' }}
          ref={provided.innerRef}
          {...provided.draggableProps}
          {...provided.dragHandleProps}
        >
          <Flex direction="column" justify="space-between" h="100%">
            <Stack direction="row" justify="space-between" align="center" mb={2}>
              <Text fontWeight="bold" fontSize="lg" noOfLines={1}>
                {todo.title}
              </Text>
              <HStack>
                <IconButton
                  icon={<ChatIcon />}
                  size="sm"
                  variant="ghost"
                  aria-label="Comments"
                />
                <IconButton
                  icon={<DeleteIcon />}
                  size="sm"
                  variant="ghost"
                  colorScheme="red"
                  aria-label="Delete"
                  onClick={deleteTodo}
                />
              </HStack>
            </Stack>
            <Text fontSize="sm" color="gray.600" noOfLines={2} mb={3}>
              {todo.description}
            </Text>
            <Box>
              <Text fontSize="sm" fontWeight="bold" mb={1}>
                Timer
              </Text>
              {!isTimerStarted ? (
                <Button
                  size="sm"
                  width="full"
                  colorScheme="blue"
                  onClick={startTimer}
                >
                  Start
                </Button>
              ) : (
                <Stack direction="row" spacing={2}>
                  <Text bg="gray.100" p={1} borderRadius="md">
                    {timer}
                  </Text>
                  <Button
                    size="sm"
                    colorScheme="blue"
                    onClick={pauseResumeTimer}
                  >
                    {pauseButton}
                  </Button>
                  <Button
                    size="sm"
                    colorScheme="red"
                    onClick={stopTimer}
                  >
                    Stop
                  </Button>
                </Stack>
              )}
            </Box>
            <Box mt={3}>
              <Flex align="center" justify="space-between" mb={1}>
                <Text fontSize="sm" fontWeight="bold">
                  Tasks
                </Text>
                <Text fontSize="xs">
                  ({numCompletedTask}/{totalTasks})
                </Text>
              </Flex>
              <Progress value={progress} size="sm" colorScheme="green" />
            </Box>
          </Flex>
        </Box>
          )}
      </Draggable>
      <TodoModal isOpen={isOpen} onClose={onClose} todo={todo}/>
      </>
  )
}
