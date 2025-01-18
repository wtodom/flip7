# DEVELOPMENT.md

## To-Do List for Next.js Project

- [x] Set up the Next.js project structure.
- [ ] Create a user profile form for inputting player strategies.
- [ ] Implement API calls to the Python backend for running simulations.
- [ ] Display simulation results in a user-friendly format.
- [ ] Create visualizations for the results using a JS library (e.g., Chart.js, Recharts).
- [ ] Implement a leaderboard for user-created profiles.
- [ ] Add functionality to save and share profiles.
- [ ] Write tests for frontend components and API integration.
- [ ] Update documentation as features are added.

## Monorepo Setup for Flip 7 Project

### Project Structure
The project will be structured as follows:

```
flip7/
├── src/ # Existing Python code
│ ├── simulation/
│ └── visualization/
├── web/ # Next.js project
│ ├── pages/
│ ├── components/
│ ├── public/
│ ├── styles/
│ ├── package.json
│ └── next.config.js
├── requirements.txt # Python dependencies
├── vercel.json # Vercel configuration
└── DEVELOPMENT.md # This document
```

### Step-by-Step Setup Process

1. **Create the Monorepo Structure**:
   - Navigate to your existing `flip7` project directory.
   - Create a new directory for the Next.js project:
     ```bash
     mkdir web
     ```

2. **Initialize the Next.js Project**:
   - Navigate into the `web` directory:
     ```bash
     cd web
     ```
   - Initialize a new Next.js project:
     ```bash
     npx create-next-app@latest .
     ```
   - Follow the prompts to set up your Next.js project.

3. **Install Additional Dependencies**:
   - If you plan to use TypeScript, install TypeScript and types:
     ```bash
     npm install --save-dev typescript @types/react @types/node
     ```

4. **Configure Vercel**:
   - Create a `vercel.json` file in the root of the project with the following content:
     ```json
     {
       "buildCommand": "cd web && npm run build",
       "outputDirectory": "web/.next",
       "devCommand": "cd web && npm run dev",
       "functions": {
         "api/*.py": {
           "runtime": "python3.9"
         }
       }
     }
     ```

5. **Set Up Python Backend**:
   - Ensure your Python backend is ready and has the necessary API endpoints to interact with the Next.js frontend.
   - Use Flask or FastAPI to create endpoints for running simulations and retrieving results.

6. **Environment Variables**:
   - Create a `.env.local` file in the `web` directory to store environment variables (e.g., API URLs).

### Development Workflow

1. **Frontend Development**:
   - Use the `web` directory for all Next.js development.
   - Run the development server:
     ```bash
     cd web
     npm run dev
     ```
   - Access the application at `http://localhost:3000`.

2. **Backend Development**:
   - Use the `src` directory for all Python backend development.
   - Run the Python server (e.g., Flask or FastAPI) separately.

3. **API Integration**:
   - Use Axios or Fetch API in your Next.js components to call the Python backend endpoints.
   - Ensure that the API calls are made to the correct URLs defined in your environment variables.

4. **Version Control**:
   - Use Git to manage changes in both the frontend and backend.
   - Commit changes regularly and push to your remote repository.

5. **Deployment**:
   - Deploy the Next.js frontend to Vercel.
   - Deploy the Python backend to a suitable platform (e.g., Heroku, DigitalOcean).

### Additional Notes
- Keep the frontend and backend codebases loosely coupled to facilitate easier maintenance and potential future separation.
- Regularly review and update the `DEVELOPMENT.md` file as the project evolves.