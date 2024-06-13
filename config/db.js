import mongoose from "mongoose";

export default function connectDB() {

  try {
    const conn =  mongoose.connect(process.env.MONGO_URL) ;
    console.log(`connection successful on url : ${process.env.MONGO_URL}`) ;
  } 

  catch (err) {
    console.error(err.message);
    process.exit(1);
  }
}
