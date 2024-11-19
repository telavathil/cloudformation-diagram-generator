import { Box } from "@mui/material";
import Editor from "@monaco-editor/react";

interface YamlEditorProps {
  value: string;
  onChange: (value: string) => void;
  generateDiagram: () => void;
}

const YamlEditor: React.FC<YamlEditorProps> = ({ value, onChange, generateDiagram }) => {
  return (
    <Box sx={{ 
      height: '100%',
      overflow: 'auto',
      border: '1px solid',
      borderColor: 'divider',
      borderRadius: 1,
      width: '100%',
    }}>
      <Editor
        height="100%"
        defaultLanguage="yaml"
        value={value}
        onChange={(value) => onChange(value || "")}
        theme="vs-dark"
        options={{
          minimap: { enabled: false },
          scrollBeyondLastLine: false,
          wordWrap: 'on',
          automaticLayout: true,
        }}
      />
    </Box>
  );
};

export default YamlEditor;
