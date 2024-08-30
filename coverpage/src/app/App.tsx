import React, { useEffect, useState } from "react";
import { Box, Button, Divider, Flex, Text, Textarea } from "@chakra-ui/react";
import { InformationInput } from "./InformationInput";
import { CoverLetterBuilder } from "./CoverLetterBuilder";
import { BeatLoader } from "react-spinners";
import Logo from "./logo.svg";

const primaryBrandColor = "#3077d2"

const App = () => {
    const [name, setName] = useState<string>("");
    const [email, setEmail] = useState<string>("");
    const [phone, setPhone] = useState<string>("");
    const [github, setGithub] = useState<string>("");
    const [linkedin, setLinkedin] = useState<string>("");

    const [companyName, setCompanyName] = useState<string>("");
    const [role, setRole] = useState<string>("");

    const [bullets, setBullets] = useState<string>("");

    const [isGenerating, setIsGenerating] = useState<boolean>(false);

    const loadData = () => {
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            const tab = tabs[0];
            if (tab.id) {
                chrome.tabs.sendMessage(
                    tab.id,
                    {
                        action: "extract_data",
                    },
                    (msg) => {
                        try {
                            const { position, company } = msg;
                            setRole(position);
                            setCompanyName(company);
                            chrome.storage.local.set({ "company-name": company, "position": position });
                        } catch (e) {
                            console.log("invalid site layout", msg)
                        }
                    }
                );
            }
        });
    };

    async function compileResume(inputString: string) {
        const url = 'https://api.resume.tonyzhou.ca/v1/compile';

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'text/plain',  // Sending raw text, not JSON
                'API-Key': "41a564e29dc84ae7972f9d8534e44a0e"
            },
            body: inputString  // Sending the raw text as body
        });

        setIsGenerating(false);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const blob = await response.blob();
        const pdfUrl = URL.createObjectURL(blob);

        const date = new Date();

        const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are 0-indexed
        const day = String(date.getDate()).padStart(2, '0');
        const year = date.getFullYear();
        const formattedDate = `${month}-${day}-${year}`;
        console.log(`${companyName}_${formattedDate}.pdf`)
        chrome.downloads.download({
            url: pdfUrl,
            filename: `${companyName}_${formattedDate}.pdf`,
            saveAs: true
        }, () => {
            URL.revokeObjectURL(url);
        });
    }

    const generate = async () => {
        setIsGenerating(true);
        const user = {
            name,
            email,
            phone,
            github,
            linkedin
        }

        const job = {
            companyName,
            role
        }

        const application = {
            bullets: bullets.split("\n")
        }

        const coverLetterBuilder = new CoverLetterBuilder(user, job, application);
        const latex = coverLetterBuilder.generateLaTeX();

        await compileResume(latex)

        setIsGenerating(false);
    }

    useEffect(() => {
        loadData();
    }, []);

    useEffect(() => {
        chrome.storage.local.get("bullets", (result) => {
            setBullets(result.bullets);
        });
    }, [])



    return (
        <Box minWidth="300px" margin="20px">
            <Flex flexDirection='column' gap="5px">
                <a href="https://atsify.vercel.app">
                    <Box display='flex' flexDirection='column' alignItems='center' onClick={() => {
                        chrome.tabs.create({ url: "https://atsify.vercel.app" });
                    }}>
                        <svg version="1.0" xmlns="http://www.w3.org/2000/svg"
                            width="70.9000000pt" height="25.7000000pt" viewBox="0 0 1399.000000 517.000000"
                            preserveAspectRatio="xMidYMid meet">

                            <g transform="translate(0.000000,517.000000) scale(0.100000,-0.100000)"
                                fill="#3077d2" stroke="none">
                                <path d="M8863 4383 c-131 -89 -323 -260 -323 -287 0 -33 317 -434 345 -435
14 -1 306 242 370 308 59 61 63 45 -65 207 -115 145 -218 254 -240 254 -10 0
-49 -21 -87 -47z"/>
                                <path d="M2025 4363 c-16 -2 -104 -12 -195 -23 -180 -22 -459 -67 -492 -79
-19 -7 -11 -17 75 -109 87 -92 96 -106 107 -157 26 -127 -21 -322 -326 -1340
-203 -674 -302 -978 -359 -1102 -35 -75 -102 -151 -225 -256 l-55 -46 453 -1
454 0 -78 63 c-194 155 -199 238 -48 774 16 57 32 103 36 103 4 0 40 -30 80
-66 93 -85 207 -160 271 -179 140 -42 252 -3 468 161 55 42 102 74 104 72 7
-6 74 -284 99 -409 28 -137 33 -239 14 -300 -16 -53 -70 -114 -134 -151 -58
-32 -64 -41 -36 -54 9 -5 282 -10 606 -12 l589 -3 -107 91 c-105 90 -107 92
-160 203 -77 158 -186 491 -509 1562 -331 1093 -362 1184 -426 1238 -29 24
-40 27 -104 26 -40 -1 -85 -4 -102 -6z m-170 -806 c35 -80 385 -1208 385
-1242 0 -16 -296 -28 -600 -23 l-215 3 2 45 c1 25 32 148 68 274 74 260 282
939 298 973 16 37 36 27 62 -30z"/>
                                <path d="M3361 4208 c-12 -84 -39 -268 -60 -408 -22 -140 -37 -257 -35 -259 2
-2 55 45 116 105 217 211 375 330 555 417 149 72 240 71 278 -4 47 -90 64
-438 64 -1319 1 -852 -18 -1223 -68 -1336 -21 -46 -40 -58 -103 -69 -37 -6
-88 -38 -77 -49 24 -24 151 -31 604 -31 460 0 535 4 535 25 0 5 -29 28 -65 50
-35 23 -86 65 -113 95 -58 63 -57 58 -72 375 -24 525 -18 1752 10 2080 13 145
27 183 81 210 134 69 388 -47 675 -307 190 -173 238 -212 250 -200 10 10 -89
672 -109 736 -16 48 -40 50 -125 12 -154 -70 -242 -76 -1087 -75 -870 1 -980
9 -1125 78 -30 14 -67 26 -81 26 -26 0 -26 -1 -48 -152z"/>
                                <path d="M7820 4324 c-96 -38 -210 -54 -455 -64 -249 -10 -366 -27 -493 -71
-110 -39 -159 -64 -250 -129 -152 -107 -291 -270 -372 -435 -77 -157 -101
-285 -81 -430 17 -124 64 -211 164 -310 128 -126 281 -227 733 -485 408 -233
555 -338 589 -422 11 -28 18 -69 17 -116 0 -64 -4 -83 -36 -147 -67 -136 -192
-242 -348 -296 -204 -70 -383 -37 -513 96 -102 104 -162 227 -232 474 -19 69
-38 131 -42 137 -4 9 -338 -602 -358 -656 -4 -11 154 -129 212 -157 167 -83
486 -144 775 -147 128 -1 153 2 215 22 95 32 293 130 390 193 112 73 278 243
334 341 123 220 174 462 126 603 -64 186 -251 340 -770 635 -473 269 -647 379
-682 432 -81 122 -33 301 122 453 159 157 331 213 513 167 210 -53 401 -180
567 -377 50 -58 91 -101 93 -96 8 25 -64 631 -89 739 -18 81 -28 85 -129 46z"/>
                                <path d="M10335 4241 c-104 -14 -160 -46 -283 -165 -115 -110 -122 -142 -122
-562 l0 -292 -27 -6 c-122 -30 -252 -70 -248 -77 3 -4 67 -43 141 -86 l136
-78 -5 -645 c-7 -896 -12 -923 -186 -1008 -42 -21 -76 -42 -76 -47 0 -18 212
-26 617 -23 421 3 441 6 397 47 -13 11 -27 21 -31 21 -17 0 -120 105 -139 142
-28 54 -39 328 -39 953 l0 520 86 29 c106 36 225 103 282 159 56 54 69 77 51
88 -8 5 -106 9 -218 9 l-203 0 5 333 c6 414 15 474 80 509 53 28 148 -45 227
-176 26 -45 59 -91 73 -104 l25 -23 30 36 c38 47 184 291 186 311 2 23 -192
100 -300 119 -102 18 -371 27 -459 16z"/>
                                <path d="M9059 3382 c-196 -103 -332 -155 -488 -188 -62 -14 -122 -29 -132
-35 -40 -21 -22 -47 73 -108 189 -122 202 -179 203 -916 0 -506 -6 -592 -46
-685 -25 -56 -50 -84 -118 -127 -39 -26 -50 -38 -42 -46 16 -16 210 -26 531
-25 339 1 435 7 435 27 0 8 -35 34 -78 57 -43 23 -85 48 -92 55 -11 11 -17 81
-25 294 -11 320 -26 893 -36 1423 -4 199 -10 362 -13 362 -3 -1 -81 -40 -172
-88z"/>
                                <path d="M11061 3377 c14 -12 60 -50 102 -85 190 -154 249 -277 605 -1262 197
-542 214 -574 325 -599 93 -20 94 -40 10 -246 -152 -373 -262 -462 -425 -345
-59 41 -121 124 -135 178 -4 18 -12 33 -18 34 -24 4 -117 -257 -178 -495 -15
-57 -15 -58 7 -73 13 -8 74 -26 137 -40 90 -21 143 -27 254 -28 138 -1 141 -1
194 29 189 105 352 445 751 1570 51 143 132 366 180 495 227 607 306 750 440
793 78 24 90 34 66 52 -33 25 -117 36 -316 42 -203 6 -416 -2 -441 -17 -11 -7
-6 -17 22 -47 116 -121 106 -247 -61 -788 -87 -279 -163 -465 -190 -465 -27 0
-134 272 -214 543 -74 251 -106 398 -106 492 0 71 4 87 45 177 25 55 45 102
45 104 0 2 -253 4 -562 4 l-563 -1 26 -22z"/>
                            </g>
                        </svg></Box></a>
                <Text variant="h3"><b>Personal Information</b></Text>
                <InformationInput storagekey="name" displayName="Name:" value={name} onChange={setName} />
                <InformationInput storagekey="email" displayName="Email:" value={email} onChange={setEmail} />
                <InformationInput storagekey="phone" displayName="Phone:" value={phone} onChange={setPhone} />
                <InformationInput storagekey="github" placeholder="github.com/username" displayName="Github:" value={github} onChange={setGithub} />
                <InformationInput storagekey="linkedin" placeholder="linkedin.com/in/username" displayName="Linkedin:" value={linkedin} onChange={setLinkedin} />
                <Divider />

                <Text variant="h3"><b>Company Information</b></Text>
                <InformationInput storagekey="company-name" displayName="Name:" value={companyName} onChange={setCompanyName} />
                <InformationInput storagekey="position" displayName="Position:" value={role} onChange={setRole} />

                <Divider />
                <Text variant="h3"><b>Bullets</b></Text>
                <Textarea size="sm" onChange={(e) => {
                    setBullets(e.target.value);
                    chrome.storage.local.set({ bullets: e.target.value });
                }}
                    value={bullets}
                >
                </Textarea>
                <Button
                    style={{ marginRight: "5px" }}
                    onClick={generate}
                    isLoading={isGenerating}
                    spinner={<BeatLoader size={8} color='white' />}
                    colorScheme='blue'

                >
                    Generate!
                </Button>
                <Text variant="h6">Please ensure all fields are filled out</Text>
            </Flex>
        </Box>
    );
};

export default App;
