import { Card, CardContent } from "@mui/material";

interface DiagramViewerProps {
  diagram: string | null;
}

const DiagramViewer: React.FC<DiagramViewerProps> = ({ diagram }) => {
  return (
    <Card sx={{ flex: 1, minWidth: 0 }}>
      <CardContent sx={{ p: 2, height: "100%" }}>
        <div className="h-full w-full flex items-center justify-center bg-gray-50 rounded">
          {diagram ? (
            <div dangerouslySetInnerHTML={{ __html: diagram }} />
          ) : (
            <p className="text-gray-400">Generated diagram will appear here</p>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default DiagramViewer;
