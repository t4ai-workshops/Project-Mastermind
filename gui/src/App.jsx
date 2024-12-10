import React, { useState, useEffect } from 'react';
import { Terminal, Split, MessageSquare, Settings, FileText, Database } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';

const MasterMindGUI = () => {
    const [activeChat, setActiveChat] = useState(null);
    const [messages, setMessages] = useState([]);
    const [memory, setMemory] = useState([]);
    const [status, setStatus] = useState('idle');

    const Sidebar = () => (
        <div className="w-64 bg-gray-100 h-screen p-4 flex flex-col">
            <div className="mb-4">
                <h2 className="text-xl font-bold mb-2">MasterMind</h2>
                <Alert>
                    <Terminal className="h-4 w-4" />
                    <AlertDescription>
                        System Ready
                    </AlertDescription>
                </Alert>
            </div>
            
            <div className="flex-1">
                <div className="mb-4">
                    <h3 className="font-medium mb-2">Active Chats</h3>
                    <div className="space-y-2">
                        {['Project Analysis', 'Code Review', 'Business Planning'].map(chat => (
                            <div 
                                key={chat}
                                className={`flex items-center p-2 rounded cursor-pointer hover:bg-gray-200 ${
                                    activeChat === chat ? 'bg-gray-200' : ''
                                }`}
                                onClick={() => setActiveChat(chat)}
                            >
                                <MessageSquare className="h-4 w-4 mr-2" />
                                <span>{chat}</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            <div className="mt-auto">
                <button className="flex items-center p-2 w-full hover:bg-gray-200 rounded">
                    <Settings className="h-4 w-4 mr-2" />
                    Settings
                </button>
            </div>
        </div>
    );

    const ChatArea = () => (
        <div className="flex-1 flex flex-col h-screen">
            <div className="flex-1 p-4 overflow-auto">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`mb-4 ${
                        msg.type === 'user' ? 'text-right' : ''
                    }`}>
                        <Card>
                            <CardContent className="p-4">
                                {msg.content}
                            </CardContent>
                        </Card>
                    </div>
                ))}
            </div>
            
            <div className="p-4 border-t">
                <textarea 
                    className="w-full p-2 border rounded-lg resize-none"
                    placeholder="Type your message..."
                    rows={3}
                />
                <div className="flex justify-between mt-2">
                    <button className="px-4 py-2 bg-gray-100 rounded">
                        <FileText className="h-4 w-4" />
                    </button>
                    <button className="px-4 py-2 bg-blue-600 text-white rounded">
                        Send
                    </button>
                </div>
            </div>
        </div>
    );

    const MemoryPanel = () => (
        <div className="w-64 bg-gray-50 h-screen p-4 border-l">
            <h3 className="font-medium mb-4 flex items-center">
                <Database className="h-4 w-4 mr-2" />
                Memory Context
            </h3>
            
            <div className="space-y-4">
                {memory.map((item, idx) => (
                    <Card key={idx}>
                        <CardContent className="p-2 text-sm">
                            <div className="font-medium">{item.category}</div>
                            <div className="text-gray-600 text-xs">
                                {item.timestamp}
                            </div>
                            <div className="mt-1">
                                {item.content}
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );

    return (
        <div className="flex h-screen bg-white">
            <Sidebar />
            <ChatArea />
            <MemoryPanel />
        </div>
    );
};

export default MasterMindGUI;