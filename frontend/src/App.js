import { Today } from './components/Today';
import { Projects } from './components/Projects'
import { ChakraProvider, Stack } from '@chakra-ui/react'
import { Side } from './components/Side';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { ProjectDetails } from './components/ProjectDetails';
import theme from './theme';
function App() {
  return (
    <ChakraProvider theme={theme}>
      <Stack
        h={'100%'}
        direction={'row'}
      >
        <BrowserRouter>
        <Side />
        <Routes>
          <Route path="/" element={<Today />} />
          <Route exact path="/projects/" element={<Projects />} />
          <Route path="/projects/:projectId" element={<ProjectDetails />}/>
        </Routes>
      </BrowserRouter>
      </Stack>
    </ChakraProvider>
  );
}

export default App;
