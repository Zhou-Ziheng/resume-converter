# ATSify

## Overview

ATSify is a web application designed to assist job seekers in converting their resumes into formats compatible with Applicant Tracking Systems (ATS) and LaTeX. This tool aims to simplify the process of creating ATS-friendly resumes by generating PDFs that are optimized for parsing by automated systems, while also providing LaTeX support for users who prefer more customization options.

## Features

- **Resume Conversion**: Convert resumes from various formats (e.g., DOCX, PDF) to ATS-friendly PDFs.
- **ATS Optimization**: Ensure the converted resumes are optimized for parsing by Applicant Tracking Systems.
- **LaTeX Support**: Generate LaTeX files for users who want to customize the appearance and layout of their resumes.
- **User-Friendly Web Interface**: Access the application via a user-friendly web interface for ease of use.

## Usage

You can access the ATSify web application by visiting [https://atsify.vercel.app/](https://atsify.vercel.app/). Simply upload your resume file and follow the on-screen instructions to convert it to an ATS-friendly format or LaTeX file.

## Running Locally

### Method 1: Cloning and Running with Python

1. Clone the repository:

    ```bash
    git clone https://github.com/Zhou-Ziheng/resume-converter.git
    cd resume-converter
    ```

2. Set the required environment variable `GEMINI_API_KEY`:

    ```bash
    export GEMINI_API_KEY=your_gemini_api_key
    ```

3. Run the application:

    ```bash
    python app.py
    ```

4. Access the application in your web browser at [http://localhost:5000](http://localhost:5000).

### Method 2: Docker Compose

1. Clone the repository:

    ```bash
    git clone https://github.com/Zhou-Ziheng/resume-converter.git
    cd resume-converter
    ```

2. Replace the placeholder `GEMINI_API_KEY` with your actual Gemini API key in the `docker-compose.yml` file.

3. Build the Docker image and start the containers:

    ```bash
    docker-compose build
    docker-compose up
    ```

4. Access the application in your web browser at [http://localhost:5000](http://localhost:5000).

## API Documentation

### POST /v1/convert

Converts a resume file to an ATS-friendly format.

#### Request

- **Method**: `POST`
- **Endpoint**: `/v1/convert`
- **Content-Type**: `multipart/form-data`

##### Parameters

| Name      | Type    | Description                                            |
|-----------|---------|--------------------------------------------------------|
| getPDF    | Boolean | Indicates whether to output a PDF (true) or a zip file (false) containing both the PDF and LaTeX files. |
| file      | File    | The resume file to be converted.                       |
| style     | JSON    | JSON object specifying the style settings for the converted resume. |

Example `style` JSON object with all fields:

```json
{
    "font_size": 12,
    "font": "FirePro",
    "header_color": "#000000",
    "subheader_color": "#333333",
    "section_header_color": "#0066CC",
    "date_color": "#666666",
    "location_color": "#666666",
    "entry_title_color": "#000000",
    "company_color": "#000000",
    "project_title_color": "#000000",
    "bullet_color": "#666666",
    "project_tools_color": "#666666",
    "skills_color": "#000000",
    "single_entry_color": "#000000"
}
```

## Contributing

Contributions to ATSify are welcome! If you encounter any bugs, have feature requests, or would like to contribute code, please open an issue or submit a pull request on the [GitHub repository](https://github.com/Zhou-Ziheng/resume-converter).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

ATSify relies on several open-source libraries and tools. We would like to thank the creators and maintainers of these projects for their valuable contributions.
