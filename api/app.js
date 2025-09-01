import 'dotenv/config'
import express from 'express';
import cors from 'cors';
import plannerRoute from '../routes/planner.route.js'
import { fileURLToPath } from 'url';
import path from 'path';
import staticRoutes from '../routes/static.route.js'

const currentFilePath = fileURLToPath(import.meta.url)
const currentDirectoryPath = path.dirname(currentFilePath);

const app = express();
console.log(currentDirectoryPath);

// Enable CORS for all routes
app.use(cors({
    origin: ['http://localhost:8081', 'http://localhost:3000', 'http://localhost:5000'],
    credentials: true
}));

app.use(express.json({limit:'16kb'}));
app.use(express.urlencoded({extended:true,limit:'16kb'}));

// Set view engine and views directory
app.set('view engine', 'ejs');
app.set('views', path.resolve(currentDirectoryPath, '..', 'view', 'pages'));

// Serve static files from the view/assets directory
app.use('/assets', express.static(path.resolve(currentDirectoryPath, '..', 'view', 'assets')));

app.use('/api', plannerRoute);
app.use('/', staticRoutes);

export default app;