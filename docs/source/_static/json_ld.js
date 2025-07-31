const script = document.createElement("script");
script.type = "application/ld+json";
script.text = JSON.stringify({
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  name: "Edgar SEC",
  url: "https://nikhilxsunder.github.io/edgar-sec/",
  description:
    "A feature-rich Python package for interacting with the US Securities and Exchange Commission API: EDGAR.",
  applicationCategory: "FinanceApplication",
  operatingSystem: "Linux, MacOS, Windows",
  softwareVersion: "2.0.0",
  author: {
    "@type": "Person",
    name: "Nikhil Sunder",
  },
  license: "https://www.gnu.org/licenses/agpl-3.0.html",
  programmingLanguage: "Python",
  downloadUrl: "https://pypi.org/project/fedfred/",
  sourceCode: "https://github.com/nikhilxsunder/fedfred",
  documentation: "https://nikhilxsunder.github.io/fedfred/",
});
document.head.appendChild(script);
