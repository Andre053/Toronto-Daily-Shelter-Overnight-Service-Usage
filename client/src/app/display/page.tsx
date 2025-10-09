import { Display } from "@/components/Display";


export default async function Home() {
  return (
    <div className="grid grid-cols-2 items-start gap-10 m-5 h-screen">
      <Display/>
    </div>
  );
};