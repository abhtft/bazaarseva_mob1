# Kirana Suvidha

A Flask web application for managing shopping lists and generating bills for Kirana shops.

## Features

- Create shopping lists with items and quantities
- Support for text, audio, and image descriptions
- Generate PDF bills
- View and manage submitted lists
- Mobile-friendly interface

## Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd kirana-suvidha
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your MongoDB connection string:
```
MONGODB_URI=your_mongodb_connection_string
```

5. Run the application:
```bash
python run.py
```

## Deployment on Render

1. Push your code to GitHub
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Set the following environment variables in Render:
   - `MONGODB_URI`: Your MongoDB connection string
5. Deploy!

## Project Structure

```
kirana_suvidha/
├── application.py      # Main application code
├── templates/         # HTML templates
│   ├── index.html     # Main form
│   ├── success.html   # Success page
│   ├── exit.html      # Exit page
│   ├── lists.html     # View lists page
│   └── view.html      # View items page
└── __init__.py        # Package initialization
```

## License

MIT License 
