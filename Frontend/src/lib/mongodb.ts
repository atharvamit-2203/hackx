// MongoDB Service for Chat History Management
import { MongoClient, Db, Collection } from 'mongodb';

interface ChatMessage {
  _id?: string;
  sessionId: string;
  userId: string;
  message: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  domain?: string;
  confidence?: number;
  sources?: string[];
  methodology?: string;
  citations?: string[];
  disclaimer?: string;
}

interface ChatSession {
  _id?: string;
  sessionId: string;
  userId: string;
  createdAt: Date;
  updatedAt: Date;
  messageCount: number;
  lastMessage?: string;
  domain?: string;
}

class MongoDBService {
  private client: MongoClient | null = null;
  private db: Db | null = null;
  private messages: Collection<ChatMessage> | null = null;
  private sessions: Collection<ChatSession> | null = null;
  
  private readonly MONGODB_URI = process.env.NEXT_PUBLIC_MONGODB_URI || 'mongodb://localhost:27017/';
  private readonly DB_NAME = 'plugmind_chat';
  private readonly MESSAGES_COLLECTION = 'messages';
  private readonly SESSIONS_COLLECTION = 'sessions';

  async connect(): Promise<void> {
    if (!this.client) {
      try {
        this.client = new MongoClient(this.MONGODB_URI);
        await this.client.connect();
        this.db = this.client.db(this.DB_NAME);
        this.messages = this.db.collection(this.MESSAGES_COLLECTION);
        this.sessions = this.db.collection(this.SESSIONS_COLLECTION);
        console.log('✅ Connected to MongoDB');
      } catch (error) {
        console.error('❌ MongoDB connection error:', error);
        throw error;
      }
    }
  }

  async disconnect(): Promise<void> {
    if (this.client) {
      await this.client.close();
      this.client = null;
      this.db = null;
      this.messages = null;
      this.sessions = null;
      console.log('✅ Disconnected from MongoDB');
    }
  }

  async createOrUpdateSession(sessionId: string, userId: string = 'default_user'): Promise<void> {
    await this.connect();
    
    const existingSession = await this.sessions?.findOne({ sessionId });
    
    if (existingSession) {
      // Update existing session
      await this.sessions?.updateOne(
        { sessionId },
        { 
          $set: { 
            updatedAt: new Date(),
            lastMessage: new Date().toISOString()
          } 
        }
      );
    } else {
      // Create new session
      await this.sessions?.insertOne({
        sessionId,
        userId,
        createdAt: new Date(),
        updatedAt: new Date(),
        messageCount: 0
      });
    }
  }

  async saveMessage(
    sessionId: string,
    userId: string,
    message: string,
    sender: 'user' | 'ai',
    metadata?: {
      domain?: string;
      confidence?: number;
      sources?: string[];
      methodology?: string;
      citations?: string[];
      disclaimer?: string;
    }
  ): Promise<void> {
    await this.connect();
    
    const chatMessage: ChatMessage = {
      sessionId,
      userId,
      message,
      sender,
      timestamp: new Date(),
      ...metadata
    };
    
    await this.messages?.insertOne(chatMessage);
    
    // Update session
    await this.sessions?.updateOne(
      { sessionId },
      { 
        $set: { 
          updatedAt: new Date(),
          lastMessage: message,
          $inc: { messageCount: 1 },
          ...(metadata?.domain && { domain: metadata.domain })
        } 
      }
    );
  }

  async getChatHistory(
    sessionId: string, 
    userId: string = 'default_user',
    limit: number = 50
  ): Promise<ChatMessage[]> {
    await this.connect();
    
    const history = await this.messages
      ?.find({ sessionId, userId })
      .sort({ timestamp: 1 })
      .limit(limit)
      .toArray() || [];
    
    return history;
  }

  async getContextMessages(
    sessionId: string,
    userId: string = 'default_user',
    contextLimit: number = 10
  ): Promise<ChatMessage[]> {
    await this.connect();
    
    const contextMessages = await this.messages
      ?.find({ sessionId, userId })
      .sort({ timestamp: -1 })
      .limit(contextLimit)
      .toArray() || [];
    
    // Return in chronological order (oldest first)
    return contextMessages.reverse();
  }

  async searchMessages(
    sessionId: string,
    userId: string = 'default_user',
    query: string,
    limit: number = 20
  ): Promise<ChatMessage[]> {
    await this.connect();
    
    const searchResults = await this.messages
      ?.find({ 
        sessionId, 
        userId,
        $or: [
          { message: { $regex: query, $options: 'i' } }
        ]
      })
      .sort({ timestamp: -1 })
      .limit(limit)
      .toArray() || [];
    
    return searchResults;
  }

  async getSessionInfo(sessionId: string): Promise<ChatSession | null> {
    await this.connect();
    
    const session = await this.sessions?.findOne({ sessionId });
    return session || null;
  }

  async deleteSession(sessionId: string, userId: string = 'default_user'): Promise<void> {
    await this.connect();
    
    // Delete messages and session
    await this.messages?.deleteMany({ sessionId, userId });
    await this.sessions?.deleteOne({ sessionId, userId });
  }

  async getAllSessions(userId: string = 'default_user'): Promise<ChatSession[]> {
    await this.connect();
    
    const sessions = await this.sessions
      ?.find({ userId })
      .sort({ updatedAt: -1 })
      .toArray() || [];
    
    return sessions;
  }

  // Generate context for AI based on recent messages
  async generateContextPrompt(
    sessionId: string,
    userId: string = 'default_user',
    maxContextMessages: number = 8
  ): Promise<string> {
    const contextMessages = await this.getContextMessages(sessionId, userId, maxContextMessages);
    
    if (contextMessages.length === 0) {
      return '';
    }
    
    let contextPrompt = 'Previous conversation context:\n\n';
    
    contextMessages.forEach((msg: ChatMessage, index: number) => {
      const sender = msg.sender === 'user' ? 'User' : 'AI Assistant';
      const timestamp = msg.timestamp.toLocaleString();
      
      contextPrompt += `[${timestamp}] ${sender}: ${msg.message}\n`;
      
      // Include domain info for AI messages
      if (msg.sender === 'ai' && msg.domain) {
        contextPrompt += `(Domain: ${msg.domain}, Confidence: ${Math.round((msg.confidence || 0) * 100)}%)\n`;
      }
    });
    
    contextPrompt += '\nCurrent question: ';
    
    return contextPrompt;
  }
}

// Export singleton instance
const mongoDBService = new MongoDBService();

export type { ChatMessage, ChatSession };
export { mongoDBService };
export default mongoDBService;
