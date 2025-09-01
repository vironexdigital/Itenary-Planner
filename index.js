import app from './api/app.js'
import logger from './utils/logger.js'

const port = process.env.PORT || 8081

app.listen(port , ()=>{
    logger.info(`Server is running on port: ${port}`)
})