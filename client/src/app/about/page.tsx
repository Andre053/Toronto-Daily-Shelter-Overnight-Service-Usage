import '../globals.css';

const Section = ({children}: {children: React.ReactNode}) => (
    <div className="mt-[36px] mx-auto">
        {children}
    </div>
)

const SectionHeading = ({children}: {children: React.ReactNode}) => (
    <h2 className="text-[26px] md:twt[36px] lg:txt[48px] font-bold text-center">
        {children}
    </h2>
)
const SectionContent = ({children}: {children: React.ReactNode}) => (
    <p className="text-[14px] leading-8 mt-8 mx-auto max-w-2xl text-justify">
        {children}
    </p>
)
const Link = ({url, children}: {url: string; children: React.ReactNode}) => (
    <a href={url} className="underline text-blue-800 hover:text-yellow-800">
        {children}
    </a>
)

export default async function Home() {

    return (
        <div className="text-center">
            <h1 className="text-[60px]">
                About
            </h1>
            <Section>
                <SectionHeading>Overview</SectionHeading>
                <SectionContent>
                    In Toronto, there are a variety of programs that aim to 
                    provide support to people in need of housing services. 
                    These services are administered by various groups, and the
                    capacity and occupancy of each is required to be tracked by 
                    the City. 
                </SectionContent>
            </Section>
            <Section>
                <SectionHeading>Objectives</SectionHeading>
                <SectionContent>
                    This website aims to be an accessible resource for those looking to better understand the 
                    programs the City has in place regarding overnight housing services, and the associated data. 
                </SectionContent>
            </Section>
            <Section>
                <SectionHeading>The data source</SectionHeading>
                <SectionContent>
                    This project explores the{' '} 
                    <Link url="https://open.toronto.ca/dataset/daily-shelter-overnight-service-occupancy-capacity/">
                        Daily Shelter & Overnight Service Occupancy & Capacity
                    </Link>
                    {' '}dataset publicized by Open Data Toronto.

                    This dataset provides information on shelter and overnight service programs ran by the City. 
                    There are various programs that are reported on, as outlined by the{' '}
                    <Link url="https://www.toronto.ca/city-government/data-research-maps/research-reports/housing-and-homelessness-research-and-reports/housing-stability-service-system-map-and-terms/">
                        Housing Stablity Service System Overview
                    </Link>
                    . This dataset is updated daily.
                </SectionContent>
            </Section>
        </div>
        
    );
};