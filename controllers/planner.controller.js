import path from 'path';
import { fileURLToPath } from 'url';
import Response from '../utils/response.js';
import logger from '../utils/logger.js';
import { spawn } from 'child_process';

export const plannerController = async(req,res)=>{
    const {text}= req.body;

    console.log("Text from the frontend is",text);

    if(!text){
        logger.error("Text from the frontend is missing");
        return res.status(400)
                .json(new Response(400,"","Invalid request"));
    }

    if(typeof(text)!=='string'){
        logger.error("The text send from the frontend is not a string");
        return res.status(400)
                .json(new Response(400,"","Invalid request"));
    }

    const currentFilePath = fileURLToPath(import.meta.url) ;
    const currentDirectoryPath = path.dirname(currentFilePath);
    const pythonFilePath = path.resolve(currentDirectoryPath,'..','services','main2.py');

    logger.info("Starting Process .......")
    
    const pythonProcess = spawn('python3',[pythonFilePath,text]);

    let result =''

    pythonProcess.stdout.on('data',(data)=>{
        result += data.toString();
    })

    pythonProcess.on("close",()=>{

        
        logger.info("Output is fetched successfully");
        logger.info("Process Ended .....")
        return res.status(200).json(new Response(200,result,"Data fetched successfully"));
    })
}