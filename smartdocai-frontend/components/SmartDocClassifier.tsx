
import { useState } from 'react';
import { Upload, FileText, CheckCircle, Loader2, Sparkles } from 'lucide-react';

export default function SmartDocClassifier() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{document_type: string, confidence: number} | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const [showCorrection, setShowCorrection] = useState(false);
  const [correction, setCorrection] = useState("");
  const [fullText, setFullText] = useState("");
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFile(e.target.files?.[0] || null);
        setResult(null);
        setFeedbackSubmitted(false);
    };

    const handleFeedbackCorrect = async () => {
    if (!result) return;

    await fetch("http://localhost:8000/feedback", {
        method: "POST",
        body: new URLSearchParams({
        text: fullText,
        predicted_label: result.document_type,
        correct_label: result.document_type,
        }),
    });
    setFeedbackSubmitted(true);
    alert("Thanks for your feedback!");
    };

    const handleSubmitCorrection = async () => {
    if (!result || !correction) return;

    await fetch("http://localhost:8000/feedback", {
        method: "POST",
        body: new URLSearchParams({
        text: fullText,
        predicted_label: result.document_type,
        correct_label: correction,
        }),
    });

    alert("Thanks! We'll use your correction to improve.");
    setShowCorrection(false);
    setCorrection("");
    };


  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragActive(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.type === 'application/pdf') {
      setFile(droppedFile);
      setResult(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/classify/", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Failed to classify document");

      const data = await res.json();
      setResult(data);
      setFullText(data.text);
    } catch (err) {
      alert("Error uploading file.");
    } finally {
      setLoading(false);
    }
  };

 return (
    <div className="w-full min-h-screen bg-gradient-to-br from-slate-300 via-gray-400 to-gray-700 flex items-center justify-center p-4">
      {/* Main Container */}
      <div className="bg-white/80 backdrop-blur-xl p-8 rounded-3xl shadow-2xl border border-white/50 w-full max-w-md relative overflow-hidden">
        
        {/* Decorative gradient background */}
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600/5 to-purple-600/5 rounded-3xl"></div>
        
        {/* Content */}
        <div className="relative z-10">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl mb-4 shadow-lg">
              <Sparkles className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent mb-2">
              SmartDoc Classifier
            </h1>
            <p className="text-gray-600 text-sm">
              AI-powered document classification
            </p>
          </div>

          {/* File Upload Area */}
          <div
            className={`
              border-2 border-dashed rounded-2xl p-8 text-center transition-all duration-300 cursor-pointer
              ${dragActive 
                ? 'border-blue-500 bg-blue-50/50 scale-105' 
                : file 
                  ? 'border-green-400 bg-green-50/50' 
                  : 'border-gray-300 hover:border-gray-400 hover:bg-gray-50/50'
              }
            `}
            onDragOver={(e) => {
              e.preventDefault();
              setDragActive(true);
            }}
            onDragLeave={() => setDragActive(false)}
            onDrop={handleDrop}
            onClick={() => document.getElementById('fileInput')?.click()}
          >
            {file ? (
              <div className="space-y-3">
                <FileText className="w-12 h-12 text-green-500 mx-auto" />
                <div>
                  <p className="font-medium text-gray-900">{file.name}</p>
                  <p className="text-sm text-gray-500">
                    {(file.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              </div>
            ) : (
              <div className="space-y-3">
                <Upload className={`w-12 h-12 mx-auto transition-colors ${dragActive ? 'text-blue-500' : 'text-gray-400'}`} />
                <div>
                  <p className="font-medium text-gray-900">
                    Drop your PDF here
                  </p>
                  <p className="text-sm text-gray-500">
                    or click to browse files
                  </p>
                </div>
              </div>
            )}
          </div>

          {/* Hidden file input */}
          <input
            id="fileInput"
            type="file"
            accept="application/pdf"
            onChange={handleFileChange}
            className="hidden"
          />

          {/* Action Button */}
          <button
            onClick={handleUpload}
            disabled={!file || loading}
            className={`
              w-full mt-6 py-4 px-6 rounded-2xl font-semibold text-white shadow-lg transition-all duration-300 transform
              ${!file || loading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 hover:scale-105 hover:shadow-xl active:scale-95'
              }
            `}
          >
            {loading ? (
              <div className="flex items-center justify-center space-x-2">
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Analyzing Document...</span>
              </div>
            ) : (
              <div className="flex items-center justify-center space-x-2">
                <Sparkles className="w-5 h-5" />
                <span>Classify PDF</span>
              </div>
            )}
          </button>

          {/* Results Display */}
          {result && (
            <>
            <div className="mt-8 p-6 bg-gradient-to-r from-green-50 to-emerald-50 rounded-2xl border border-green-200">
              <div className="flex items-center space-x-3 mb-4">
                <CheckCircle className="w-6 h-6 text-green-600" />
                <h3 className="text-lg font-semibold text-green-900">
                  Classification Complete
                </h3>
              </div>
              
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-700 font-medium">Document Type:</span>
                  <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-semibold">
                    {result.document_type}
                  </span>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-gray-700 font-medium">Confidence:</span>
                  <div className="flex items-center space-x-2">
                    <div className="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-gradient-to-r from-green-500 to-emerald-500 transition-all duration-1000"
                        style={{ width: `${result.confidence * 100}%` }}
                      ></div>
                    </div>
                    <span className="text-sm font-semibold text-gray-900">
                      {(result.confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
              </div>
            </div>
                {/* Feedback Section */}
                <div className="mt-6">
                <p className="text-sm font-medium text-gray-700 mb-2">
                    Was this classification correct?
                </p>

                {!showCorrection ? (
                    <div className="flex gap-3">
                    <button
                        onClick={handleFeedbackCorrect}
                        disabled={feedbackSubmitted}
                        className={!feedbackSubmitted ?"px-4 py-2 rounded-xl bg-green-600 text-white hover:bg-green-700 transition": ""}
                    >
                        Yes
                    </button>
                    <button
                        onClick={() => setShowCorrection(true)}
                        className="px-4 py-2 rounded-xl bg-red-500 text-white hover:bg-red-600 transition"
                    >
                        No
                    </button>
                    </div>
                ) : (
                    <div className="space-y-3 mt-3">
                    <input
                        type="text"
                        placeholder="Enter correct label"
                        className="w-full p-2 border rounded-xl"
                        value={correction}
                        onChange={(e) => setCorrection(e.target.value)}
                    />
                    <button
                        onClick={handleSubmitCorrection}
                        disabled={!correction}
                        className="px-4 py-2 rounded-xl bg-blue-600 text-white hover:bg-blue-700 transition disabled:opacity-50"
                    >
                        Submit Correction
                    </button>
                    </div>
                )}
                </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
