import madge from "madge";

const getFilesDependencies = (path, config) => {
  const dependencies = madge(path, config);
  return JSON.stringify(dependencies);
};

module.exports = {
  getFilesDependencies,
};
