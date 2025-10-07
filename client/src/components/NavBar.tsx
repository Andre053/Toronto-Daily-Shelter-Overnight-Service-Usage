'use client'
import Link from "next/link"

const LinkItem = ({children, href}: {children: React.ReactNode; href: string; }) => (
    <Link
        href={href}
        className=""
    >
        {children}
    </Link>
)

export const NavBar = () => (
    <nav className="sticky top-0 w-full flex items-center justify-between bg-indigo-800 p-1 text-[26px] text-white font-bold border-b-7 border-indigo-900">
        <Link href="/" className="ml-5">
            LOGO HERE
        </Link>
        <ul className="flex items-center gap-8 mt-2 mb-2 mr-5">
            <LinkItem href="/story">
                Story
            </LinkItem>  
            <LinkItem href="/display">
                Explore
            </LinkItem>  
            <LinkItem href="/charts">
                Charts
            </LinkItem>   
            <LinkItem href="/about">
                About
            </LinkItem>                
        </ul>
    </nav>
)