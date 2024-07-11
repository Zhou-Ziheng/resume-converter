import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { Box, Button, Divider, Flex, Text, Textarea } from "@chakra-ui/react";
import { InformationInput } from "./InformationInput";
import { set } from "lodash";
import { CoverLetterBuilder } from "./CoverLetterBuilder";

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
                        console.log(msg)
                        const { position, company } = msg;
                        setRole(position);
                        setCompanyName(company);
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
        window.open(pdfUrl);
    }

    const generate = () => {
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
        console.log(latex);

        compileResume(latex)


    }

    useEffect(() => {
        loadData();
    }, []);

    useEffect(() => {
        chrome.storage.local.get("bullets", (result) => {
            console.log(result.bullets);
            setBullets(result.bullets);
        });
    }, [])



    return (
        <Box minWidth="300px" margin="20px">
            <Flex flexDirection='column' gap="5px">
                <Text variant="h3">Personal Information</Text>
                <InformationInput storagekey="name" displayName="Name:" value={name} onChange={setName} />
                <InformationInput storagekey="email" displayName="Email:" value={email} onChange={setEmail} />
                <InformationInput storagekey="phone" displayName="Phone:" value={phone} onChange={setPhone} />
                <InformationInput storagekey="github" placeholder="github.com/username" displayName="Github:" value={github} onChange={setGithub} />
                <InformationInput storagekey="linkedin" placeholder="linkedin.com/in/username" displayName="Linkedin:" value={linkedin} onChange={setLinkedin} />
                <Divider />

                <Text variant="h3">Company Information</Text>
                <InformationInput storagekey="company-name" displayName="Name:" value={companyName} onChange={setCompanyName} />
                <InformationInput storagekey="position" displayName="Position:" value={role} onChange={setRole} />

                <Divider />
                <Text variant="h3">Bullets</Text>
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
                    disabled={isGenerating}
                    
                >
                    Generate!
                </Button>
            </Flex>
        </Box>
    );
};

export default App;
