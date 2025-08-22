import 'dotenv/config'
import express from 'express';
import plannerRoute from '../routes/planner.route.js'
import { fileURLToPath } from 'url';
import path from 'path';
import staticRoutes from '../routes/static.route.js'

const currentFilePath = fileURLToPath(import.meta.url)
const currentDirectoryPath = path.dirname(currentFilePath);


const app = express();

app.use(express.json({limit:'16kb'}));
app.use(express.urlencoded({extended:true,limit:'16kb'}));

app.set('view engine',"ejs")
app.set("views",path.resolve(currentDirectoryPath,'..','view','pages'))

app.use('/api',plannerRoute)
app.use('/',staticRoutes)

export default app;