import React, { useState } from "react";
import CodeMirror from "@uiw/react-codemirror";
import { yaml } from "@codemirror/lang-yaml";
import { oneDark } from "@codemirror/theme-one-dark";
import { Card, CardContent } from "@mui/material";
import Button from "@mui/material/Button";

interface YamlEditorProps {
  value: string;
  onChange: (value: string) => void;
  generateDiagram: () => void;
}

const YamlEditor: React.FC<YamlEditorProps> = ({
  value,
  onChange,
  generateDiagram,
}) => {
  const [error, setError] = useState<string | null>(null);

  const handleChange = React.useCallback(
    (val: string) => {
      onChange(val);
    },
    [onChange]
  );

  return (
    <div className="flex flex-col lg:flex-row h-screen p-4 gap-4">
      {/* Editor Section */}
      <Card sx={{ flex: 1, minWidth: 0 }}>
        <CardContent sx={{ p: 2, height: "100%" }}>
          <div className="flex flex-col h-full gap-4">
            <CodeMirror
              value={value}
              height="100%"
              extensions={[yaml()]}
              onChange={(value) => onChange(value)}
              className="flex-1 border rounded"
            />
            {error && <p className="text-red-500 text-sm">{error}</p>}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default YamlEditor;
