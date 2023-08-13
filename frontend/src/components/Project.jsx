import {
    Heading, 
    Text,
    WrapItem,
    Card,
    CardBody,
    Image,
    Tag
    } from '@chakra-ui/react'
import { Link } from 'react-router-dom'

  export const Project = ({project}) => {

    const updateField = (e, fieldName) => {
        // update
    }

    const updateProject = () => {
        // update project
    }
    return(
      <>
        <WrapItem key={project.id}>
        <Card w={'200px'} h={'250px'}>
          <Image src="https://via.placeholder.com/150x75"/>
          <Link to={`/projects/${project.id}`}>
          <CardBody>
            <Tag
                borderRadius='full'
                variant='solid'
                bg={project.color}
            />
            <Heading as={'h2'} size={'md'}>{project.name}</Heading>
            <Text>{project.description.length > 40 ? project.description.substring(0, 40)+'...': project.description }</Text>
          </CardBody>
           </Link>
        </Card>
      </WrapItem>
    </>
    )
  }