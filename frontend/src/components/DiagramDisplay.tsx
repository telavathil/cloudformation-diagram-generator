import React from 'react';
import { Box } from '@mui/material';

interface DiagramDisplayProps {
  svgContent: string;
}

const DiagramDisplay: React.FC<DiagramDisplayProps> = ({ svgContent }) => {
  return (
    <Box
      sx={{
        width: '100%',
        height: '100%',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        overflow: 'auto',
        '& svg': {
          width: '100%',
          height: '100%',
          maxWidth: '100%',
          maxHeight: '100%',
          objectFit: 'contain',
        },
        '& image': {
          width: '96px !important',
          height: '96px !important',
        },
        '& text': {
          fontSize: '14px !important',
          fontFamily: '"Monaco", "Menlo", monospace !important',
          textAnchor: 'middle !important',
          dominantBaseline: 'text-after-edge !important',
          dy: '1.5em !important',
        },
        '& .edge text': {
          fontSize: '12px !important',
          dominantBaseline: 'middle !important',
        }
      }}
      dangerouslySetInnerHTML={{
        __html: svgContent,
      }}
    />
  );
};

export default DiagramDisplay;