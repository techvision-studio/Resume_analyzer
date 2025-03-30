import { useState } from "react";

const ResumeUpload = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [responseData, setResponseData] = useState(null);

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const handleFileUpload = async () => {
        if (!selectedFile) {
            alert("Please select a file first!");
            return;
        }

        const formData = new FormData();
        formData.append("file", selectedFile);

        try {
            const response = await fetch("http://127.0.0.1:8000/analyze-resume/", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            setResponseData(data);
            console.log("Server Response:", data);
        } catch (error) {
            console.error("Upload Error:", error);
            setResponseData({ error: "Failed to upload file." });
        }
    };

    return (
        <div>
            <h2>Upload Resume</h2>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleFileUpload}>Upload</button>

            {responseData && (
                <div>
                    <h3>Analysis Result:</h3>
                    {responseData.error ? (
                        <p style={{ color: "red" }}>{responseData.error}</p>
                    ) : (
                        <div>
                            <p><strong>Filename:</strong> {responseData.filename}</p>
                            <p><strong>Skills:</strong> {responseData.skills.join(", ")}</p>
                            <p><strong>Education:</strong> {responseData.education.join(", ")}</p>
                            <p><strong>Contact:</strong> {JSON.stringify(responseData.contact_info)}</p>
                            <p><strong>Extracted Text:</strong> {responseData.extracted_text}</p>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default ResumeUpload;
