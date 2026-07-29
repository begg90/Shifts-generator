input/output needs to be independent
it is convenient to start with these two formats because 
- csv and json packages are python native
- they are easy to generate and read also in streamlit
- csv is good for table type data, eg list of personnel
- json can handle non tabular type data, eg. multiple roles

these data type can be good to prototype our project.
in a second phase we can migrate to SQL
(which might solve the problem of streamlit not caching the previous sessions!)