"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import styles from "./page.module.css";
const names = ["tony", "elias", "fadi"];

export default function Home() {
  const [text, setText] = useState("");
  const [typewriterText, setTypewriterText] = useState("");
  const apiText =
    "tet consul imperdiet te vix. Per in integre meliore vituperata, ea veniam saperet vis, no pro probo regione lobortis. Ei vim putent dolorem elaboraret, ei perfecto consectetuer duo. Duo an aliquam similique signiferumque. In duo brute etiam, an mea paulo efficiendi, mea alii ludus te. Ea prima quando mel, lorem aeque alterum vel ut, et est unum necessitatibus. Mea ad causae voluptua atomorum, mel modo putant dissentias at.";
  // Simulating fetching text from an API
  useEffect(() => {
    //fetchYourTextFromAPI().then((fetchedText) => setText(fetchedText));

    setText(apiText);
  }, []);

  useEffect(() => {
    let index = 0;
    const timer = setInterval(() => {
      setTypewriterText(
        (prevTypewriterText) => prevTypewriterText + text.charAt(index)
      );
      index++;
      if (index === text.length) {
        clearInterval(timer);
      }
    }, 10); // adjust timing here

    return () => clearInterval(timer); // cleanup on unmount
  }, [text]);

  return (
    <div className={styles.main}>
      <div>{typewriterText}</div>
    </div>
  );
}

/*

    <main className={styles.main}>
      <div className={styles.description}>
        <p>
          Get started by editing&nbsp;
          <code className={styles.code}>src/app/page.js</code>
        </p>
        <div>
          <a
            href="https://vercel.com?utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
            target="_blank"
            rel="noopener noreferrer"
          >
            By{" "}
            <Image
              src="/vercel.svg"
              alt="Vercel Logo"
              className={styles.vercelLogo}
              width={100}
              height={24}
              priority
            />
          </a>
        </div>
      </div>

      <div className={styles.center}>
        <Image
          className={styles.logo}
          src="/next.svg"
          alt="Next.js Logo"
          width={180}
          height={37}
          priority
        />
      </div>

      <div className={styles.grid}>
        <a
          href="https://nextjs.org/docs?utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
          className={styles.card}
          target="_blank"
          rel="noopener noreferrer"
        >
          <h2>
            Docs <span>-&gt;</span>
          </h2>
          <p>Find in-depth information about Next.js features and API.</p>
        </a>

        <a
          href="https://nextjs.org/learn?utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
          className={styles.card}
          target="_blank"
          rel="noopener noreferrer"
        >
          <h2>
            Learn <span>-&gt;</span>
          </h2>
          <p>Learn about Next.js in an interactive course with&nbsp;quizzes!</p>
        </a>

        <a
          href="https://vercel.com/templates?framework=next.js&utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
          className={styles.card}
          target="_blank"
          rel="noopener noreferrer"
        >
          <h2>
            Templates <span>-&gt;</span>
          </h2>
          <p>Explore starter templates for Next.js.</p>
        </a>

        <a
          href="https://vercel.com/new?utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
          className={styles.card}
          target="_blank"
          rel="noopener noreferrer"
        >
          <h2>
            Deploy <span>-&gt;</span>
          </h2>
          <p>
            Instantly deploy your Next.js site to a shareable URL with Vercel.
          </p>
        </a>
      </div>
    </main>

    */
