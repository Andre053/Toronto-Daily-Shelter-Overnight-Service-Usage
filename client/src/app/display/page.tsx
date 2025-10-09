import { Display } from "@/components/DisplayPage";

// old styles: "grid grid-cols-2 items-start gap-10 m-5 h-screen"
export default async function Home() {
  return (
    <div className="grid grid-cols-1 items-top justify-top content-start gap-2 m-5 h-screen">
      <Display/>
    </div>
  );
};