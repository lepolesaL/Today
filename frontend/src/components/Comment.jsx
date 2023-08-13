import {
  Box, 
  Text} from '@chakra-ui/react';
import React, { } from 'react';
import { DeleteIcon, EditIcon} from '@chakra-ui/icons';

  export const Comment = ({comment,  date, key}) => {

    return(
      <Box mb={2} bg={'gray.200'} rounded={'base'} gap={2} p={2}>
        <Box display='flex' justifyContent={'space-between'} alignItems={'center'}>
          <Text fontSize={'xs'} as='i'>{new Date(date).toISOString()}</Text>
          <Box>
            <EditIcon />
            <DeleteIcon />
          </Box>
        </Box>
        <Text key={key}>{comment}</Text>
      </Box>
    )
  }