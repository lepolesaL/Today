import {
    Heading, 
    Stack  } from '@chakra-ui/react'
import { Droppable } from 'react-beautiful-dnd'
import React from 'react';
import { Todo } from './Todo';
import axios from 'axios';

export const Column = ({index, column, tasks, updateColumns}) => {

  const deleteTodoFromColumn = async(index) => {
    var col = column
    col.todos.splice(index, 1)
    let response = await axios.patch(`${process.env.REACT_APP_API_URL}/columns/${col.id}/`, col.todos)
    if (response.status) {
      updateColumns(col)
    }
  }
  return(
    <Droppable
      key={column.id}
      droppableId={column.id}
      >
      {(provided, snapshot) => (
     <Stack
     borderWidth="1px"
     borderRadius="lg"
     p={4}
     bg={`${column.color}.50`}
     boxShadow="md"
     overflowY="auto"
     maxHeight="calc(100vh - 200px)"
     ref={provided.innerRef}
     {...provided.droppableProps}
   >
     <Heading as="h3" fontSize="xl" textAlign="center" mb={4} color={`${column.color}.700`}>
       {column.name.toUpperCase()}
     </Heading>
     {provided.placeholder}
     {tasks.length > 0 && tasks.map((task, index) => (
       <Todo
         key={task.id}
         todo={task}
         index={index}
         columnId={column.id}
         deleteFromColumn={deleteTodoFromColumn}
       />
     ))}
   </Stack>
      )}
    </Droppable>
  )
}