import express from 'express';
import {plannerController} from '../controllers/planner.controller.js'

const router = express.Router();

router.post('/generate-plan',plannerController);

export default router;