import { Inter, Roboto } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

const robot = Roboto({
  subsets: ["latin"],
  weight: ["100", "300", "400", "500", "700"],
});

export const metadata = {
  title: "Skygarden Deveops Netsec",
  description: "AI",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={robot.className}>{children}</body>
    </html>
  );
}
