import './App.css';
import React, { useState } from "react";
import '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css';
import { MainContainer, ChatContainer, MessageList, Message, MessageInput, TypingIndicator } from '@chatscope/chat-ui-kit-react'
import axios from 'axios'
import { FaCheck, FaTimes, FaInfoCircle } from 'react-icons/fa';
import "./styles.css"



function App() {
  const [isChatbotTyping, setIsChatbotTyping] = useState(false);
  const [username, setUsername] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [hoveredItem, setHoveredItem] = useState(null);
  const [itemStates, setItemStates] = useState({
    LLMBasedSecurity: false,
    GuardrailsPrior: false,
    GuardrailsAfter: false,
    LLMJudge: false,
    GDPR: false,
  });

  const info_on_items = {
    LLMBasedSecurity: "Instructs the LLM to maintain confidentiality by only providing information about the logged-in user, ensuring no private data about other employees is disclosed",
    GuardrailsPrior: "Applies guardrails to the user query before issuing the prompt to the LLM", 
    GuardrailsAfter: "Applies guardrails to the LLM's response after the prompt is issued, ensuring the output adheres to security policies",
    LLMJudge: "Evaluates and ensures that the responses generated by a language model comply with predefined criteria or guidelines. This will be checked by a second call to an LLM.",
    GDPR: "Checks whether the language model understands and applies GDPR rules to the query"
  };

  const models= ["gpt-3.5-turbo", "gpt-4o", "mistral-small-latest", "Meta-Llama-3-8B-Instruct-4bit"]
  const [selectedModel, setSelectedModel] = useState(models[0]);
  const [modelDropdownState, setModelDropdownState] = useState(false);

  const toggleItem = (item) => {
    setItemStates(prevState => ({
      ...prevState,
      [item]: !prevState[item]
    }));
  };

  const handleSelectModel = (model) => {
    setSelectedModel(model);
    setModelDropdownState(!modelDropdownState);
  }

  // State to store chat messages
  const [chatMessages, setChatMessages] = useState([
    {
      message: "Hello, I am the company's chatbot! How can I assist you?",
      sender: "ChatGPT",
      direction: "incoming"
    },
  ]);

  const handleLogin = (e) => {
    e.preventDefault();
    if (username.trim()) {
      setIsLoggedIn(true);
    }
  };

  const handleUserMessage = async (userMessage) => {
    // Create a new user message object
    const newUserMessage = {
      message: userMessage,
      sender: "user",
      direction: "outgoing",
    };
 
    // Update chat messages state with the new user message
    const updatedChatMessages = [...chatMessages, newUserMessage];
    setChatMessages(updatedChatMessages);
 
    // Set the typing indicator for the chatbot
    setIsChatbotTyping(true);
 
    // Process user message with ChatGPT
    await handleSend(newUserMessage,updatedChatMessages)
    setIsChatbotTyping(false);
  };

  const handleSend = async (message, messages) => {
    try {
      const res = await axios.post('http://127.0.0.1:5000/complete', {
        prompt: message,
        username: username,
        guard_rail_before: itemStates.GuardrailsPrior,
        guard_rail_after: itemStates.GuardrailsAfter,
        llm_safety: itemStates.LLMBasedSecurity,
        llm_judge: itemStates.LLMJudge,
        gdpr: itemStates.GDPR,
        model: selectedModel
      });
      setChatMessages([
        ...messages,
        {
          message: res.data,
          sender: "ChatGPT",
          direction: "incoming"
        },
      ]);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <>
      {!isLoggedIn ? (
        // Login Screen
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
          <form onSubmit={handleLogin} style={{ textAlign: 'center' }}>
            <h2>Login</h2>
            <input
              type="text"
              placeholder="Enter your username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              style={{ padding: '10px', fontSize: '16px', width: '200px' }}
            />
            <button type="submit" style={{ padding: '10px 20px', fontSize: '16px', marginTop: '10px' }}>
              Login
            </button>
          </form>
        </div>
      ) : (
        // Chat Screen
        <div style={{ position: "relative", height: "100vh", width: "100%", flexDirection: 'column'}}>
  <MainContainer>
    <div style={{ display: 'flex', flexDirection: 'column', backgroundColor: 'white'}}>
      
      <div style={{ textAlign: 'center' }}>
        <h3 style={{ margin: '10px 0 0 0' }}>Security Layer</h3>
      </div>
      
      <div
        className="dropdown-items"
        style={{
          position: "relative", // Changed from absolute to relative for proper stacking
          zIndex: 10, // Lower zIndex to place below the dropdown
          backgroundColor: "#fff",
          border: "1px solid #ccc",
          boxShadow: "0 2px 10px rgba(0, 0, 0, 0.1)",
          marginBottom: '10px' // Add some spacing between the dropdowns
        }}
      >
        {Object.keys(itemStates).map(item => (
          <div className="dropdown-item" key={item}>
            <div
              className="dropdown__link"
              onClick={() => toggleItem(item)}
              style={{ 
                display: "flex", 
                alignItems: "center", 
                justifyContent: "space-between", // Ensures the text and icon are on opposite sides
                padding: '8px', 
                whiteSpace: 'nowrap', 
                width: '100%', 
                boxSizing: "border-box" 
              }} 
            >
              <div style={{ display: "flex", alignItems: "center" }}>
                <span style={{ marginRight: "10px" }}>
                  {itemStates[item] ? <FaCheck color="green" /> : <FaTimes color="red" />}
                </span>
                {item.replace("item", "Item ")}
              </div>
              
              <div
                style={{ position: "relative", display: 'flex', alignItems: 'center'}}
                onMouseEnter={() => setHoveredItem(item)}
                onMouseLeave={() => setHoveredItem(null)}
              >
                <FaInfoCircle style={{color: 'lightskyblue'}}/>
                {hoveredItem === item && (
                  <div
                    style={{
                      position: "absolute",
                      left: "100%", // Position the tooltip to the right of the icon
                      top: "50%",
                      transform: "translateX(10px) translateY(-50%)", // Adjust positioning
                      backgroundColor: "white",
                      border: "1px solid #ccc",
                      padding: "5px",
                      borderRadius: "4px",
                      boxShadow: "0 2px 8px rgba(0, 0, 0, 0.15)",
                      whiteSpace: "nowrap",
                      zIndex: 1
                    }}
                  >
                    {info_on_items[item]}
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div style={{ textAlign: 'center' }}>
        <h3 style={{ margin: '0 0 0 0' }}>LLM Model</h3>
      </div>

      <div
        className="dropdown"
        style={{
          position: "relative",
          zIndex: 20, // Higher zIndex to place above the other dropdown
        }}
      >
        <div
          className="dropdown-items"
          style={{
            backgroundColor: "#fff",
            border: "1px solid #ccc",
            boxShadow: "0 2px 10px rgba(0, 0, 0, 0.1)",
            marginBottom: '10px', // Add some spacing
          }}
        >
          {models.map((model, index) => (
            <div className="dropdown-item" key={index}>
              <div
                className="dropdown__link"
                onClick={() => handleSelectModel(model)}
                style={{ 
                  display: "flex", 
                  alignItems: "center", 
                  padding: '8px' 
                }} 
              >
                <span style={{ marginRight: "10px" }}>
                  {selectedModel === model ? <FaCheck color="green" /> : <FaTimes color="red" />}
                </span>
                {model}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>

    <ChatContainer>
      <MessageList
        typingIndicator={
          isChatbotTyping ? (
            <TypingIndicator content="Our chatbot is thinking" />
          ) : null
        }
      >
        {chatMessages.map((message, i) => {
          return (
            <Message
              key={i}
              model={message}
              style={
                message.sender === "ChatGPT"
                ? { textAlign: "left" }
                : { textAlign: "right" }
              }
            />
          );
        })}
      </MessageList>
      <MessageInput
        placeholder="Type Message here"
        onSend={handleUserMessage}
      />
    </ChatContainer>
  </MainContainer>
</div>

      )}
    </>
  );

}

export default App;
