import React, { useState } from "react";
import { Box, Container, Stack, useTheme, useMediaQuery, Typography, Button } from "@mui/material";
import { ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import { theme } from './theme/theme';
import DiagramDisplay from './components/DiagramDisplay';
import YamlEditor from "./components/YamlEditor";



const App: React.FC = () => {
  const [yamlContent, setYamlContent] = useState("");
  const [svgContent, setSvgContent] = useState<string | null>(null);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("md"));

  const handleSubmit = async () => {
    try {
      const response = await fetch("http://localhost:5001/generate-diagram", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ yaml: yamlContent }),
      });

      if (response.headers.get("content-type")?.includes("image/svg+xml")) {
        const svgText = await response.text();
        setSvgContent(svgText);
      } else {
        const data = await response.json();
        console.error("Error:", data.error);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container 
        maxWidth={false}
        sx={{ 
          height: '100vh',
          width: '100vw',
          display: 'flex',
          flexDirection: 'column',
          p: 3,
        }}
      >
        <Typography 
          variant="h3" 
          component="h1" 
          textAlign="center" 
          color="primary.main" 
          mb={3}
        >
          CloudFormation Diagram Generator
        </Typography>
        <Stack
          direction={{ xs: "column", md: "row" }}
          spacing={3}
          sx={{
            flex: 1,
            overflow: 'hidden'
          }}
        >
          <Box sx={{ 
            flex: 1, 
            minWidth: 0,
            display: 'flex',
            flexDirection: 'column' 
          }}>
            <Box sx={{ flex: 1, overflow: 'hidden' }}>
              <YamlEditor
                value={yamlContent}
                onChange={setYamlContent}
                generateDiagram={handleSubmit}
              />
            </Box>
            <Button
              variant="contained"
              onClick={handleSubmit}
              sx={{
                mt: 2,
                bgcolor: 'primary.main',
                color: 'white',
                '&:hover': {
                  bgcolor: 'primary.dark',
                },
              }}
            >
              Generate Diagram
            </Button>
          </Box>

          <Box
            sx={{
              flex: 1,
              minWidth: 0,
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              border: "1px solid",
              borderColor: 'divider',
              borderRadius: 1,
              p: 2,
              bgcolor: 'background.paper',
              overflow: "auto",
            }}
          >
            {svgContent ? (
              <DiagramDisplay svgContent={svgContent} />
            ) : (
              <Typography
                color="text.secondary"
                fontSize="1.2rem"
                textAlign="center"
                p={2}
              >
                Your diagram will appear here
              </Typography>
            )}
          </Box>
        </Stack>
      </Container>
    </ThemeProvider>
  );
};

export default App;
