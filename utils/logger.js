class Logger {
    info(message){
        console.info(`[INFO]: ${message}`)
    }

    warn(message){
        console.warn(`[WARN]: ${message}`)
    }

    error(message){
        console.error(`[ERROR]: ${message}`)
    }
}

const logger = new Logger();

export default logger;