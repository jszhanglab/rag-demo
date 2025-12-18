interface PDFViewerProps {
  ocrText: string;
}

const PDFViewer: React.FC<PDFViewerProps> = ({ ocrText }) => {
  return (
    <div>
      <h2>OCR Text</h2>
      <div>{ocrText}</div>
    </div>
  );
};

export default PDFViewer;
