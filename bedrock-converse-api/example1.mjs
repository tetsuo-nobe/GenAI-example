import {
  BedrockRuntimeClient,
  ConverseCommand,
} from "@aws-sdk/client-bedrock-runtime";

const client = new BedrockRuntimeClient({ region: "us-east-1" });

const userMessage = "Explain 'rubber duck debugging' in one line.";

const conversation = [
  {
    role: "user",
    content: [{ text: userMessage }],
  },
];

//const modelId = "anthropic.claude-3-haiku-20240307-v1:0";
//const modelId = "amazon.titan-text-express-v1";
//const modelId = "ai21.j2-mid-v1";
const modelId = "cohere.command-light-text-v14";

const command = new ConverseCommand({
  modelId,
  messages: conversation
});

const response = await client.send(command);

const responseText = response.output.message.content[0].text;
console.log(responseText);

