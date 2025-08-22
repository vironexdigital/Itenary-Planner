import express from 'express';

const route = express.Router();

route.get('/',async(req,res)=>{
    res.render('index')
})

route.get('/plan',async(req,res)=>{
    res.render('PlanningPage')
})

export default route