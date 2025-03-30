import React from "react";
import { Container, Card } from "react-bootstrap";

const ResumeAnalysisResult = ({ data }) => {
  if (!data) return null;

  return (
    <Container className="mt-4">
      <h3>Analysis Result</h3>
      <Card>
        <Card.Body>
          <h5>Extracted Skills:</h5>
          <p>{data.skills.join(", ")}</p>

          <h5>Education:</h5>
          <p>{data.education}</p>

          <h5>Contact Information:</h5>
          <p>{data.contact_info}</p>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default ResumeAnalysisResult;
