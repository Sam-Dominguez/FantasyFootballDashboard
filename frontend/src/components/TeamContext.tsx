import React, { createContext, useState, useContext, ReactNode } from 'react';

// Define the context type
interface TeamContextType {
  selectedTeamId: string;
  setSelectedTeamId: (id: string) => void;
}

// Define the type for the props of TeamProvider, including the children prop
interface TeamProviderProps {
  children: ReactNode;
}

// Create the context with the type
const TeamContext = createContext<TeamContextType | undefined>(undefined);

export const TeamProvider: React.FC<TeamProviderProps> = ({ children }) => {
  const [selectedTeamId, setSelectedTeamId] = useState<string>("__");

  return (
    <TeamContext.Provider value={{ selectedTeamId, setSelectedTeamId }}>
      {children}
    </TeamContext.Provider>
  );
};

export const useTeamContext = () => {
  const context = useContext(TeamContext);
  if (!context) {
    throw new Error("useTeamContext must be used within a TeamProvider");
  }
  return context;
};
