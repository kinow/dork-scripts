XML ELEMENT

    public static void main(String[] args) {
        Class<?> clazz = java.lang.invoke.MethodHandles.lookup().lookupClass();
        java.lang.reflect.Method[] methods = clazz.getMethods();
        StringBuilder sb = new StringBuilder();
        StringBuilder sb2 = new StringBuilder();
        int methodIndex = 0;
        java.util.List<String[]> tuples = new java.util.ArrayList<>();
        for (java.lang.reflect.Method method : methods) {
            java.lang.annotation.Annotation[] annotations = method.getAnnotations();
            for (java.lang.annotation.Annotation annotation : annotations) {
                Class<? extends java.lang.annotation.Annotation> annotationType = annotation.annotationType();
                if ("javax.xml.bind.annotation.XmlElement".equals(annotationType.getName())) {
                    // found a method that needs to be tested
                    XmlElement xmlElementAnnotation = method.getAnnotation(XmlElement.class);
                    String name = xmlElementAnnotation.name();
                    String methodName = method.getName();
                    tuples.add(new String[] {name, methodName});
                }
            }
        }
        java.util.Collections.sort(tuples, (a, b) -> a[0].compareTo(b[0]));
        for (String[] entry : tuples) {
            sb.append(String.format("assertEquals(\"%s\", nodeList.item(%d).getNodeName());", entry[0], methodIndex));
            sb.append(System.getProperty("line.separator"));
            sb2.append(String.format("assertEquals(po.%s().toString(), nodeList.item(%d).getTextContent());", entry[1], methodIndex));
            sb2.append(System.getProperty("line.separator"));
            methodIndex += 1;
        }
        System.out.println(sb.toString());
        System.out.println(sb2.toString());
    }

XML ATTRIBUTE

    public static void main(String[] args) {
        Class<?> clazz = java.lang.invoke.MethodHandles.lookup().lookupClass();
        java.lang.reflect.Method[] methods = clazz.getMethods();
        StringBuilder sb = new StringBuilder();
        StringBuilder sb2 = new StringBuilder();
        java.util.List<String[]> tuples = new java.util.ArrayList<>();
        for (java.lang.reflect.Method method : methods) {
            java.lang.annotation.Annotation[] annotations = method.getAnnotations();
            for (java.lang.annotation.Annotation annotation : annotations) {
                Class<? extends java.lang.annotation.Annotation> annotationType = annotation.annotationType();
                if ("javax.xml.bind.annotation.XmlAttribute".equals(annotationType.getName())) {
                    // found a method that needs to be tested
                    XmlAttribute xmlElementAnnotation = method.getAnnotation(XmlAttribute.class);
                    String name = xmlElementAnnotation.name();
                    String methodName = method.getName();
                    tuples.add(new String[] {name, methodName});
                }
            }
        }
        java.util.Collections.sort(tuples, (a, b) -> a[0].compareTo(b[0]));
        for (String[] entry : tuples) {
            sb.append(String.format("assertEquals(\"%s\", namedNodeMap.getNamedItem(\"%s\").getNodeName());", entry[0], entry[0]));
            sb.append(System.getProperty("line.separator"));
            sb2.append(String.format("assertEquals(po.%s().toString(), namedNodeMap.getNamedItem(\"%s\").getTextContent());", entry[1], entry[0]));
            sb2.append(System.getProperty("line.separator"));
        }
        System.out.println(sb.toString());
        System.out.println(sb2.toString());
    }