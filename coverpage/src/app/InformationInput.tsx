import { Box, Input, Text } from "@chakra-ui/react";
import React, { useEffect } from "react"

interface InformationInputProps {
    storagekey: string;
    value: string;
    onChange: (value: string) => void;
    displayName: string;
    placeholder?: string;
}

export const InformationInput = ({ placeholder, displayName, storagekey, value, onChange }: InformationInputProps) => {

    const [isEditing, setIsEditing] = React.useState(false);

    useEffect(() => {
        chrome.storage.local.get([storagekey], function (result) {
            if (result[storagekey]) {
                onChange(result[storagekey]);
            }
        }
        );
    }, [])

    return <Box display='flex' alignItems='center'>
        <Text variant="h5" width="70px">{displayName}</Text>
        <Input size='sm'
            type="text"
            value={value}
            placeholder={placeholder}
            onChange={(e) => {
                onChange(e.target.value);
                chrome.storage.local.set({ [storagekey]: e.target.value });
            }}
        />
    </Box>
}
