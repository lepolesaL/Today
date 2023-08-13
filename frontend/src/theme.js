import { extendTheme } from '@chakra-ui/react'

const colors = {
  brand: {
    primary: '#7C8363',
    secondary: '#A4B494',
    accent: '#BFCBA8',
    light: '#FAFDF7',
    dark: '#3B3C36',
  },
}

const fonts = {
  heading: '"Poppins", sans-serif',
  body: '"Open Sans", sans-serif',
}

const styles = {
  global: {
    body: {
      bg: 'brand.light',
      color: 'brand.dark',
    },
  },
}

const components = {
  Button: {
    baseStyle: {
      fontWeight: 'bold',
      borderRadius: 'full',
    },
    variants: {
      solid: (props) => ({
        bg: props.colorScheme === 'brand' ? 'brand.primary' : undefined,
        color: props.colorScheme === 'brand' ? 'white' : undefined,
        _hover: {
          bg: props.colorScheme === 'brand' ? 'brand.secondary' : undefined,
        },
      }),
    },
  },
  Card: {
    baseStyle: {
      container: {
        boxShadow: 'md',
        borderRadius: 'lg',
      },
    },
  },
}

const theme = extendTheme({ colors, fonts, styles, components })

export default theme