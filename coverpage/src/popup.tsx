import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { Box, Button } from "@chakra-ui/react";
import { ChakraProvider } from '@chakra-ui/react'
import App from "./app/App";

const Popup = () => {
  return (
    <ChakraProvider>
      <App />
    </ChakraProvider>
  );
};

const root = createRoot(document.getElementById("root")!);

root.render(
  <React.StrictMode>
    <Popup />
  </React.StrictMode>
);
