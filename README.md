# 🔑 AI API Key Tester

A simple, beautiful web application to test API keys for various AI providers including OpenAI, Anthropic, Google AI, and Mistral AI.

## 🚀 Features

- **Multi-Provider Support**: Test API keys for OpenAI, Anthropic, Google AI, and Mistral AI
- **Real-time Testing**: Makes actual API calls to verify key validity
- **Secure Input**: Password-type inputs to protect your API keys
- **Beautiful UI**: Modern, responsive design with gradient backgrounds
- **Instant Feedback**: Clear success/error messages with detailed information
- **Keyboard Shortcuts**: Use Ctrl+1/2/3/4 to quickly focus on different provider inputs
- **Mobile Friendly**: Responsive design that works on all devices

## 📋 Supported Providers

### OpenAI
- **API Endpoint**: `https://api.openai.com/v1/models`
- **Authentication**: Bearer token
- **Test Method**: Lists available models
- **Key Format**: `sk-...`

### Anthropic
- **API Endpoint**: `https://api.anthropic.com/v1/messages`
- **Authentication**: x-api-key header
- **Test Method**: Makes a simple chat completion request
- **Key Format**: `sk-ant-...`

### Google AI (Gemini)
- **API Endpoint**: `https://generativelanguage.googleapis.com/v1beta/models`
- **Authentication**: Query parameter
- **Test Method**: Lists available models
- **Key Format**: `AIza...`

### Mistral AI
- **API Endpoint**: `https://api.mistral.ai/v1/models`
- **Authentication**: Bearer token
- **Test Method**: Lists available models
- **Key Format**: Your Mistral API key

## 🛠️ How to Use

1. **Open the Application**: Open `index.html` in your web browser
2. **Enter API Keys**: Input your API keys in the respective provider sections
3. **Test Keys**: Click the "Test [Provider] Key" button for each provider
4. **View Results**: Check the results section for success/error messages

### Keyboard Shortcuts
- `Ctrl+1` or `Cmd+1`: Focus OpenAI key input
- `Ctrl+2` or `Cmd+2`: Focus Anthropic key input
- `Ctrl+3` or `Cmd+3`: Focus Google AI key input
- `Ctrl+4` or `Cmd+4`: Focus Mistral key input

## 🔧 Technical Details

### Architecture
- **Frontend**: Pure HTML, CSS, and JavaScript (no frameworks)
- **API Calls**: Uses Fetch API for making HTTP requests
- **Styling**: Modern CSS with gradients and responsive design
- **Security**: API keys are handled client-side only

### Browser Requirements
- Modern browsers with ES6+ support
- Fetch API support
- HTTPS required for API calls (automatically handled by browsers)

### Error Handling
- Network errors
- Invalid API keys
- Rate limiting
- CORS issues
- Malformed responses

## 📁 File Structure

```
Simple API KEY Tester/
├── index.html              # Main application file
├── API_KEY_TESTER_README.md # This documentation
└── README.md              # Project overview
```

## 🔒 Security Considerations

- **Client-Side Only**: API keys are processed entirely in the browser
- **No Storage**: Keys are not saved or transmitted to any server
- **HTTPS Required**: All API calls use HTTPS for security
- **Password Fields**: API key inputs are masked for privacy

## 🚨 Important Notes

### Rate Limiting
- Be aware of API rate limits when testing keys
- Some providers may charge for API calls
- Test responsibly and monitor your usage

### CORS Policy
- Some APIs may have CORS restrictions
- If you encounter CORS errors, the API may not allow browser-based requests
- Consider using a backend proxy for production applications

### API Changes
- AI provider APIs can change over time
- Monitor provider documentation for updates
- The application may need updates if API endpoints change

## 🐛 Troubleshooting

### Common Issues

**"Network Error"**
- Check your internet connection
- Verify the API endpoint is accessible
- Some providers may block browser requests due to CORS

**"Invalid Key"**
- Double-check your API key format
- Ensure the key is active and not expired
- Verify you have the correct permissions

**"CORS Error"**
- The API doesn't allow browser-based requests
- Use a backend service or proxy for testing
- Check the provider's CORS policy

### Browser Console
- Open browser developer tools (F12)
- Check the Console tab for detailed error messages
- Network tab shows request/response details

## 🤝 Contributing

This is a simple tool, but contributions are welcome:

1. Fork the repository
2. Add new AI providers
3. Improve the UI/UX
4. Add more comprehensive error handling
5. Submit a pull request

## 📄 License

This project is open source. Feel free to use, modify, and distribute.

## 🙏 Acknowledgments

- Built with ❤️ for the AI developer community
- Inspired by the need for quick API key validation
- Uses modern web technologies for a smooth experience

## 📞 Support

If you encounter issues or have suggestions:

1. Check the troubleshooting section above
2. Open an issue on GitHub
3. Review the browser console for error details

---

**Happy testing! 🎉**
