import React, { useRef, useState } from 'react';
import { uploadDocument } from '../services/api';
import './DocumentUpload.css';

const DocumentUpload = ({ userId }) => {
  const fileInputRef = useRef(null);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);

  const handleFileSelect = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Check file type
    const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
    if (!allowedTypes.includes(file.type)) {
      setUploadStatus({ type: 'error', message: 'Please upload a PDF, DOCX, or TXT file' });
      return;
    }

    setUploading(true);
    setUploadStatus(null);

    try {
      const result = await uploadDocument(userId, file);
      setUploadStatus({
        type: 'success',
        message: `Document "${file.name}" uploaded successfully! ${result.chunks} chunks processed.`
      });
      
      // Clear file input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (error) {
      setUploadStatus({
        type: 'error',
        message: `Upload failed: ${error.message}`
      });
    } finally {
      setUploading(false);
      // Clear status after 5 seconds
      setTimeout(() => setUploadStatus(null), 5000);
    }
  };

  return (
    <div className="document-upload">
      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf,.docx,.txt"
        onChange={handleFileSelect}
        style={{ display: 'none' }}
        disabled={uploading}
      />
      <button
        onClick={() => fileInputRef.current?.click()}
        disabled={uploading}
        className="upload-button"
        title="Upload document"
      >
        {uploading ? '⏳' : '📄'}
      </button>
      {uploadStatus && (
        <div className={`upload-status ${uploadStatus.type}`}>
          {uploadStatus.message}
        </div>
      )}
    </div>
  );
};

export default DocumentUpload;

