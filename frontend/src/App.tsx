import React, { useState } from "react";
import YamlEditor from "./components/YamlEditor";
import "./App.css";
import { Box, Container, Stack, useTheme, useMediaQuery } from "@mui/material";
import { ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";

const DiagramDisplay: React.FC<{ svgContent: string }> = ({ svgContent }) => {
  return (
    <div
      dangerouslySetInnerHTML={{
        __html: svgContent,
      }}
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        overflow: "auto",
      }}
    />
  );
};

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
      <Container maxWidth="xl">
        <Box sx={{ py: 3 }}>
          <h1>CloudFormation Diagram Generator</h1>
          <Stack
            direction={{ xs: "column", md: "row" }}
            spacing={3}
            sx={{
              minHeight: "calc(100vh - 150px)",
              mt: 3,
            }}
          >
            {/* Editor Section */}
            <Box sx={{ flex: 1, minWidth: 0 }}>
              <YamlEditor
                value={yamlContent}
                onChange={setYamlContent}
                generateDiagram={handleSubmit}
              />
              <Box sx={{ mt: 2 }}>
                <button className="submit-button" onClick={handleSubmit}>
                  Generate Diagram
                </button>
              </Box>
            </Box>

            {/* Diagram Display Section */}
            <Box
              sx={{
                flex: 1,
                minWidth: 0,
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                border: "1px solid #ccc",
                borderRadius: "4px",
                padding: "16px",
                backgroundColor: "#fff",
                overflow: "hidden",
              }}
            >
              {svgContent ? (
                <DiagramDisplay svgContent={svgContent} />
              ) : (
                <div className="placeholder">Your diagram will appear here</div>
              )}
            </Box>
          </Stack>
        </Box>
      </Container>
    </ThemeProvider>
  );
};

export default App;
