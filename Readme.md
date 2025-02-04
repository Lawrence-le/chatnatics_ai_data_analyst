# Chatnatics: The AI Data Analyst

## Objective

Chatnatics aims to provide users with insightful data analysis through a conversational interface. By leveraging local language and openai models, users can interact with the chatbot to analyze datasets, gain insights, and make data-driven decisions.

## Description

Chatnatics is an AI-powered chatbot designed to assist users in data analysis tasks. The application integrates OpenAI's API and a Local Language Processing Model to process and interpret user inputs, providing contextual responses based on dataset queries. The project emphasizes prompt validation, ensuring that only relevant inputs are processed for analysis.

## Features

- **Conversational Data Analysis**
- **Prompt Validation for Contextual Relevance**
- **Real-time Data Insights**
- **User-friendly Interface with TailwindCSS Styling**

## Tech Stack

### Frontend

- **React**
- **Redux**
- **Axios**
- **TailwindCSS**

### Backend

- **Flask**
- **Pandas**
- **Numpy**
- **Scikit-Learn**
- **OpenAI API Integration**
- **RESTful API**

### Testing and Containerization

- **Docker**
- **Pytest**

## System Architecture

![Chatnatics Architecture](<public/System%20Architecture%20(OpenAI-ML_DA).jpg>)

The system comprises:

1. **Frontend:** Built with React and Redux for state management, Axios for API communication, and TailwindCSS for responsive design.
2. **Backend:** Flask serves as the main framework, handling API requests, integrating data analysis libraries like Pandas, Numpy, and Scikit-Learn, and interacting with the OpenAI API.
3. **Validation Logic:** User prompts are validated to ensure relevance to data analysis. Non-relevant prompts are guided back on track, ensuring effective utilization of OpenAI's capabilities.
4. **Testing & Deployment:** Docker is used for containerization, while Pytest ensures robust testing.

## Prompt Validation Implementation

To maintain context and provide accurate analysis:

- **Input Validation:** Every user prompt is validated against predefined criteria to ensure relevance.
- **Contextual Guidance:** If a prompt is deemed irrelevant, the chatbot provides feedback to guide users back to relevant inquiries.
- **Selective LLM Processing:** Only validated prompts are forwarded to the OpenAI API, ensuring efficient, contextually accurate responses. This validation process enhances cost efficiency by filtering out irrelevant inputs, ensuring only meaningful context is passed instead of forwarding everything the user prompts.

## Open Source Data

Chatnatics leverages publicly available datasets from [data.gov.sg](https://data.gov.sg/) to enhance analytical capabilities. Specifically, it utilizes the **[Graduate Employment Survey - NTU, NUS, SIT, SMU, SUSS & SUTD (2013-2022)](https://data.gov.sg/datasets?page=1&query=graduate+employment&coverage=&resultId=d_3c55210de27fcccda2ed0c63fdd2b352)** dataset. This dataset provides valuable insights into graduate employment trends, enabling users to analyze job market outcomes and salary distributions across different universities and disciplines.

## Expanding Local Language Processing Use Cases

The use of a local language processing model in Chatnatics is not limited to data analysis. This model can be extended to other digital solutions across various industries, such as banking, e-commerce, CRM systems, and more. By enabling seamless interactions in local languages, businesses can provide more personalized and efficient customer experiences across diverse sectors.
