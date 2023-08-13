import {
  Container,
  Heading,
  Stack,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  useDisclosure,
  Button,
  Textarea,
  Text,
  Input,
  Wrap,
  WrapItem,
  Card,
  CardBody
} from '@chakra-ui/react'
import { AddIcon } from '@chakra-ui/icons'
import { useEffect, useState } from 'react'
import { CompactPicker } from 'react-color'
import axios from 'axios'
import { Project } from './Project'

export const Projects = () => {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [projects, setProjects] = useState([])
  const { isOpen, onOpen, onClose } = useDisclosure()
  const [projectColor, setProjectColor] = useState('#fff')
  const [isLoading, setIsLoading] = useState(true)

  const addProject = () => {
    if (!!name && !!description) {
      axios.post(`${process.env.REACT_APP_API_URL}/projects/`, {
        name,
        description,
        color: projectColor
      }).then((response) => {
        var id = response.id
        var newProject = {}
        newProject.id = id
        newProject.name = name
        newProject.color = projectColor
        newProject.description = description
        setProjects(prev => [newProject, ...prev])
      })
    }
  }

  useEffect(() => {
    const loadProject = () => {
      axios.get(`${process.env.REACT_APP_API_URL}/projects/`)
        .then((response) => {
          setProjects(response.data)
          setIsLoading(false)
        })
    }
    isLoading && loadProject()
  }, [isLoading])

  return (
    <>
      <Container maxWidth="container.xl" py={10}>
        <Heading
          fontSize={{ base: '3xl', md: '4xl', lg: '5xl' }}
          textAlign="center"
          fontWeight="bold"
          color="gray.100"
          mb={8}
        >
          Projects
        </Heading>
        <Wrap spacing={6} justify="center">
          <WrapItem>
            <Card
              w="200px"
              h="250px"
              onClick={onOpen}
              _hover={{ transform: 'scale(1.05)', transition: 'all 0.2s' }}
              cursor="pointer"
            >
              <CardBody>
                <Stack align="center" justify="center" h="100%" w="100%">
                  <AddIcon boxSize={10} color="gray.500" />
                </Stack>
              </CardBody>
            </Card>
          </WrapItem>
          {projects.map(project => (
            <Project key={project.id} project={project} />
          ))}
        </Wrap>
      </Container>
      <Modal isOpen={isOpen} size={'lg'} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Add Project</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <Stack p={2} gap={2}>
              <Text>Name:</Text>
              <Input placeholder='Add todo name' defaultValue={""} onChange={e => setName(e.currentTarget.value)} />
              <Stack>
                <Text>Description:</Text>
                <Textarea onChange={e => setDescription(e.currentTarget.value)} />
              </Stack>
              <CompactPicker color={projectColor} onChangeComplete={(e) => setProjectColor(e.hex)} />
            </Stack>
          </ModalBody>
          <ModalFooter>
            <Button mr={3} onClick={onClose}>
              Close
            </Button>
            <Button colorScheme='blue' variant='ghost' onClick={addProject}>Save</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  )
}