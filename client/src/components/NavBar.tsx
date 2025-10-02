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
    <nav className="sticky top-0 w-full flex items-center justify-between bg-blue-400 text-[26px] border-b-3">
        <Link href="/" className="ml-5">
            LOGO HERE
        </Link>
        <ul className="flex items-center gap-8 mt-2 mb-2 mr-5">
            <LinkItem href="/story">
                Story
            </LinkItem>  
            <LinkItem href="/explore">
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