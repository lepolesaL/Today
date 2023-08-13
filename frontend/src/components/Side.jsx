import React, { useEffect, useState } from 'react';
import {
  Box, 
  Heading, 
  Text,
  Divider,
  List,
  ListItem,
  ListIcon,
  Flex,
  Link as ChakraLink
} from '@chakra-ui/react';
import { MdDashboardCustomize } from "react-icons/md";
import { Gi3DHammer } from 'react-icons/gi';
import { Link as ReactRouterLink } from 'react-router-dom';
import axios from 'axios';
import pusher from '../pusher';

const emoji = {
  good: "😊",
  moderate: "😐",
  bad: "🙁",
  worse: "😡"
};

export const Side = () => {
  const [selectedEmoji, setSelectedEmoji] = useState('good');

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_URL}/progress_indicator/`)
      .then((response) => {
        const progressIndicator = response.data;
        setSelectedEmoji(progressIndicator.progress_status);
      })
      .catch((error) => console.error(error));
  }, []);

  useEffect(() => {
    const channel = pusher.subscribe('todos');
    channel.bind('event', data => {
      setSelectedEmoji(data.progress_status);
    });

    return () => {
      pusher.unsubscribe('todos');
    };
  }, []);


  return (
    <Box
      bg="brand.primary"
      opacity={0.9}
      w={{ base: '100%', md: '20%', lg: '15%' }}
      h="100vh"
      position="sticky"
      top={0}
      left={0}
      boxShadow="lg"
    >
      <Flex direction="column" h="100%" py={10}>
        <Flex direction="column" align="center" mb={8}>
          <Text fontSize="6xl" mb={2}>{emoji[selectedEmoji]}</Text>
          <Heading size="lg" color="white">Today</Heading>
        </Flex>
        <Divider mb={6} />
        <List spacing={4} px={4}>
          <ListItem>
            <ChakraLink as={ReactRouterLink} to='/' _hover={{ color: 'brand.accent' }}>
              <ListIcon as={MdDashboardCustomize} boxSize={5} color="white" />
              <Text color="white" display="inline-block" ml={2}>Dashboard</Text>
            </ChakraLink>
          </ListItem>
          <ListItem>
            <ChakraLink as={ReactRouterLink} to='/projects' _hover={{ color: 'brand.accent' }}>
              <ListIcon as={Gi3DHammer} boxSize={5} color="white" />
              <Text color="white" display="inline-block" ml={2}>Projects</Text>
            </ChakraLink>
          </ListItem>
        </List>
      </Flex>
    </Box>
  )
}