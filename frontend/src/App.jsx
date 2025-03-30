import { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css"; // ✅ Import Bootstrap
import MyNavbar from "./components/Navbar";
import ResumeUpload from "./components/ResumeUpload";
import ResumeAnalysisResult from "./components/AnalysisResult";

const App = () => {
  const [analysisData, setAnalysisData] = useState(null);

  return (
    <>
      {/* Navbar */}
      <MyNavbar />

      <div className="container mt-4">
        <h1 className="text-center">Resume Analyzer</h1>

        {/* Resume Upload Component */}
        <ResumeUpload onUpload={setAnalysisData} />

        {/* Resume Analysis Result Component */}
        <ResumeAnalysisResult data={analysisData} />
      </div>
    </>
  );
};

export default App;
